from utils.base_transformer import BaseTransformer
from core.exceptions import (
    MissingSourceColumnsError,
    InvalidHeadersError
)
import polars as pl
import re 

class InversionTransformer(BaseTransformer):
    required_columns = {"pais", "cod_pais", "flujo", "pais_aladi", "pais_banrep"}
    required_headers = {"pais", "cod_pais", "pais_aladi", "flujo", "pais_banrep"}

    column_mapping = {
        "pais": "pais",
        "pais_banrep": "pais_banrep",
        "cod_pais": "cod_pais",
        "pais_aladi": "pais_aladi",
        "flujo": "flujo",
    }
    

    def __init__(self):
        super().__init__(destination_table="ban_rep_inversion")

    def _validate_headers(self, df: pl.DataFrame):
        file_columns = set(df.columns)
        
        missing_required = self.required_headers - file_columns
        if missing_required:
            raise InvalidHeadersError(list(missing_required), list(file_columns))
        
        year_cols = [c for c in df.columns if re.match(r"^\d{4}(_?(pre|pro))?$", c)]
        if not year_cols:
            raise InvalidHeadersError(
                ["Al menos una columna de año (1994, 1995, ..., 2025, etc)"],
                list(file_columns)
            )

    def _map_columns(self, df: pl.DataFrame) -> pl.DataFrame:
        # Verificar que existan las columnas de mapeo requeridas
        required_cols = self.required_headers
        missing_source_cols = required_cols - set(df.columns)
        if missing_source_cols:
            raise MissingSourceColumnsError(list(missing_source_cols))

        # Identificar columnas de años (números de 4 dígitos con opcionales sufijos 'pre'/'pro')
        year_cols = [c for c in df.columns if re.match(r"^\d{4}(_?(pre|pro))?$", c)]
        
        # Columnas a mantener: las requeridas + las de años
        cols_to_keep = list(self.required_headers) + year_cols
        
        # Seleccionar solo las columnas relevantes
        df = df.select(cols_to_keep)
        
        return df

    def _transform(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Convierte de formato pivotado (años como columnas) a formato normalizado.
        Resultado: una fila por país, año y flujo.
        """
        # Identificar columnas de años (considerando sufijos pre/pro)
        year_columns = [c for c in df.columns if re.match(r"^\d{4}(_?(pre|pro))?$", c)]
        
        # Columnas de índice (no se pivotan) - incluir todas las columnas que no son años
        index_cols = [c for c in df.columns if c not in year_columns]

        # Hacer unpivot para convertir años a filas
        df = df.unpivot(
            index=index_cols,
            on=year_columns,
            variable_name="fecha_col",
            value_name="valor"
        )
        
        # Extraer el año (números) de la columna fecha_col
        # Esto maneja tanto "1994" como "2020 pre" -> se extrae "1994" o "2020"
        df = df.with_columns(
            pl.col("fecha_col").str.extract(r"(\d{4})", 1).cast(pl.Int32).alias("fecha")
        )
        
        # Opcionalmente, extraer el tipo de dato (pre, pro, o vacío)
        df = df.with_columns(
            pl.col("fecha_col").str.extract(r"(pre|pro)?$", 1).alias("tipo_dato")
            .fill_null("actual")  # Si no tiene sufijo, es dato actual
        )
        
        # Descartar la columna fecha_col original, ya no necesaria
        df = df.drop("fecha_col")
        
        return df
    

    
