from app.utils.base_transformer import BaseTransformer
import polars as pl

class PaisesTransformer(BaseTransformer):
    required_columns = {
        "cod_pais",
    }

    column_mapping = {
        "cod._pais":"cod_pais",
        "pais_(aladi)":"pais",
        "aladi":"aladi",
        "aec":"aec",
        "alianza_del_pacifico":"ap",
        "america_latina_y_el_caribe":"alc",
        "caricom":"caricom",
        "celac":"celac",
        "comunidad_andina":"comunidad_andina",
        "efta":"efta",
        "mercosur":"mercosur",
        "tlc_estados_unidos":"tlc_eu",
        "triangulo_norte":"tn",
        "union_europea":"ue",
        "total_acuerdos_comerciales":"tac",
        "zonas_francas":"zf"
    }

    def __init__(self):
        super().__init__(destination_table="codigo_pais_acuerdos")

    def _transform(self, df: pl.DataFrame) -> pl.DataFrame:
        # Eliminar filas donde cod_pais sea null
        df = df.filter(pl.col("cod_pais").is_not_null())

        # Eliminar duplicados por cod_pais
        # df = df.unique(subset=["cod_pais"], keep="first")
        return df
    

    
