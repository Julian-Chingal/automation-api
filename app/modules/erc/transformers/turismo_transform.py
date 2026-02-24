from utils.base_transformer import BaseTransformer
import polars as pl

class TurismoTransformer(BaseTransformer):
    required_columns = {
        "anio",
        "pais",
        "codigo_pais",
        "viajeros",
        "mes",
        "flujo",
    }

    column_mapping = {
        "año": "anio",
        "mes": "mes",
        "cod_país":"codigo_pais",
        "país_turismo": "pais",
        "viajeros": "viajeros",
        "flujo_turismo": "flujo",
    }

    def __init__(self):
        super().__init__(destination_table="visitas_turismo")

    def _transform(self, df: pl.DataFrame) -> pl.DataFrame:
        group_cols = ["anio", "mes", "codigo_pais", "pais", "flujo"]
        df_aggregated = df.group_by(group_cols).agg(
            pl.col("viajeros").sum()
        )
        
        return df_aggregated
    

    
