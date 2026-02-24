from abc import ABC, abstractmethod
from core.exceptions import (
    AppException,
    TransformationError,
    MissingSourceColumnsError,
    MissingRequiredColumnsError,
    InvalidHeadersError,
)
import polars as pl
import unicodedata

class BaseTransformer(ABC):
    required_columns: set[str] = set()
    column_mapping: dict[str, str] = {}

    def __init__(self, destination_table: str):
        self._destination_table = destination_table


    def transform(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Transforms the input DataFrame and returns the transformed DataFrame.
        """
        try:
            df = self._clean(df)
            self._validate_headers(df)
            df = self._map_columns(df)
            self._validate_required_columns(df)
            df = self._transform(df)
            return df
        except AppException:
            raise

        except Exception as e:
            raise TransformationError(
                message="Unexpected error during transformation.",
                details={"original_error": str(e)},
            ) from e
            
    
    def _clean(self, df: pl.DataFrame) -> pl.DataFrame:
        def normalize_column_name(col: str) -> str:
            # Remover acentos
            col = unicodedata.normalize("NFD", col)
            col = "".join(c for c in col if unicodedata.category(c) != "Mn")
            # Convertir a minúsculas y reemplazar espacios
            col = col.strip().lower().replace(" ", "_")
            return col
        
        new_columns = [normalize_column_name(col) for col in df.columns]
        return df.rename(dict(zip(df.columns, new_columns)))
    
    def _validate_headers(self, df: pl.DataFrame):
        """
        Valida que el archivo contenga todos los encabezados (headers) esperados en la primera fila.
        Si el archivo no tiene los headers esperados, lanza InvalidHeadersError.
        """
        if not self.column_mapping:
            return
        
        expected_columns = set(self.column_mapping.keys())
        file_columns = set(df.columns)
        
        missing_cols = expected_columns - file_columns
        if missing_cols:
            raise InvalidHeadersError(list(missing_cols), list(file_columns))
    
    def _map_columns(self, df: pl.DataFrame):
        """
        Aplica el mapeo de columnas definido en `column_mapping` al DataFrame. Si no se han definido columnas requeridas, devuelve el DataFrame sin cambios. Si faltan columnas de origen para el mapeo, lanza un error.
        """
        if not self.required_columns:
            return df
        
        missing_source_cols = set(self.column_mapping.keys()) - set(df.columns)

        if missing_source_cols:
            raise MissingSourceColumnsError(list(missing_source_cols))
        
        df = df.select(list(self.column_mapping.keys()))
        return df.rename(self.column_mapping)

    
    def _validate_required_columns(self, df: pl.DataFrame):
        """
        Valida que todas las columnas requeridas estén presentes en el DataFrame.
        """
        missing_columns = self.required_columns - set(df.columns)
        if missing_columns:
            raise MissingRequiredColumnsError(list(missing_columns))
    
    @abstractmethod
    def _transform(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Método abstracto que debe ser implementado por las clases hijas para realizar la transformación específica.
        """
        ...

    @property
    def destination_table(self) -> str:
        """
        Devuelve el nombre de la tabla de destino.
        """
        return self._destination_table