from core.exceptions import InvalidHeadersError, MissingSourceColumnsError
from utils.base_transformer import BaseTransformer
import polars as pl
import re

YEAR_COL_PATTERN = re.compile(r"^\d{4}(-p)?$", re.IGNORECASE)

class BienesTransformer(BaseTransformer):
    required_columns = {"cod_pais", "nandina", "departamento", "flujo", "periodo"}
    
    column_mapping = {
        "cod_pais": "cod_pais",
        "pais": "pais",
        "nandina": "nandina",
        "descripcion_resumida": "descripcion_resumida",
        "ambito": "ambito",
        "mineros/no_mineros": "mineros_no_mineros",
        "departamento": "departamento",
        "flujo": "flujo",
        "periodo":"periodo",
    }

    def __init__(self):
        super().__init__(destination_table="comercio_bienes")

    def _validate_headers(self, df: pl.DataFrame):
        if not self.column_mapping:
            return
        
        expected_columns = set(self.column_mapping.keys())
        file_columns = set(df.columns)
        
        missing_cols = expected_columns - file_columns
        if missing_cols:
            raise InvalidHeadersError(list(missing_cols), list(file_columns))
        
    def _map_columns(self, df):
        # Verificar que existan las columnas de mapeo requeridas
        static_source_cols = list(self.column_mapping.keys())
        missing = set(static_source_cols) - set(df.columns)

        if missing:
            raise MissingSourceColumnsError(list(missing))

        # Identificar columnas de años (números de 4 dígitos con opcionales sufijos '-P')
        year_cols = [c for c in df.columns if YEAR_COL_PATTERN.match(c)]

        # Seleccionar solo las columnas relevantes
        df = df.select(static_source_cols + year_cols)

        # Renombrar solo las estáticas (los años quedan igual)
        df = df.rename(self.column_mapping)
        
        return df

    def _transform(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Convierte de formato pivotado (años como columnas) a formato normalizado.
        Resultado: una fila por país, año y flujo.
        """
        # Identificar columnas de años (considerando sufijos -P)
        year_columns = [c for c in df.columns if YEAR_COL_PATTERN.match(c)]

        # Columnas de índice (no se pivotan) - incluir todas las columnas que no son años
        index_cols = [c for c in df.columns if c not in year_columns]

        # Hacer unpivot para convertir años a filas
        df = df.unpivot(
            index=index_cols,
            on=year_columns,
            variable_name="anio_col",
            value_name="valor"
        )
        
        # Extraer el año (números) de la columna fecha_col
        # Esto maneja tanto "1994" como "2020 pre" -> se extrae "1994" o "2020"
        df = df.with_columns(
            pl.col("anio_col").str.extract(r"(\d{4})", 1).cast(pl.Int16).alias("anio")
        )
        
        # Extraer el tipo de dato (p o vacío)
        df = df.with_columns(
            pl.col("anio_col")
            .str.contains(r"(?i)-p$")
            .alias("es_preliminar")
        )
        
        # Descartar la columna fecha_col original, ya no necesaria
        df = df.drop("anio_col")

        # Limpiar valores: reemplazar coma decimal y castear
        df = df.with_columns(
            pl.col("valor")
              .cast(pl.Utf8)
              .str.replace(",", ".")
              .cast(pl.Float64)
              .alias("valor")
        )

        # Eliminar filas donde valor es null (años sin dato)
        # df = df.filter(pl.col("valor").is_not_null())
        
        return df