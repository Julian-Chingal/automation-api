from utils.base_transformer import BaseTransformer
import polars as pl

class ServiciosTransformer(BaseTransformer):
    required_columns = {
        "flujo_comercial",
        "periodo_mes",
        "codigo_cabps",
        "cod_pais",
        "cod_depto",
    }

    column_mapping = {
        "cod_pais":"cod_pais",
        "pais_serv":"nombre_pais",
        "pais_aladi":"pais_aladi",
        "flujo_comercial":"flujo_comercial",
        "periodo_mes":"periodo_mes",
        "codigo_cabps":"codigo_cabps",
        "descripcion_cabps":"descripcion_cabps",
        "cod_depto":"cod_depto",
        "nombre_departamento":"nombre_departamento",
        "usd_millones":"millones_dolares",
    }

    def __init__(self):
        super().__init__(destination_table="emces_servicios")

    def _transform(self, df: pl.DataFrame) -> pl.DataFrame:
        group_cols = ["flujo_comercial", "periodo_mes", "codigo_cabps", "cod_pais", "cod_depto"]
        df_aggregated = df.group_by(group_cols).agg(
            pl.col("millones_dolares").sum()
        )
        return df_aggregated
    

    
