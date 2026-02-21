from utils.base_transformer import BaseTransformer
import polars as pl

class TurismoTransformer(BaseTransformer):
    required_columns = {
        "anio",
        "pais",
        "viajeros",
        "mes",
        "flujo",
        "codigo_pais",
    }

    column_mapping = {
        "año": "anio",
        "país": "pais",
        "viajeros": "viajeros",
        "mes": "mes",
        "flujo": "flujo",
        "código_pais": "codigo_pais",
    }

    def __init__(self):
        super().__init__(destination_table="visitas_turismo")

    def _transform(self, df: pl.DataFrame) -> pl.DataFrame:
        return df
    

    
