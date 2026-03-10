from app.utils.base_transformer import BaseTransformer
import polars as pl

class EjecucionPresupuestalTransformer(BaseTransformer):
    required_columns = {
       "uej", "rubro", "fecha", "rec"
    }

    column_mapping = {
        "uej": "uej",
        "nombre_uej": "nombre_uej",
        "rubro": "rubro",
        "tipo": "tipo",
        "cta": "cta",
        "sub_cta": "subcta",
        "obj": "obj",
        "ord": "ord",
        "sor_ord": "sorord",
        "item": "item",
        "sub_item": "subitem",
        "fuente": "fuente",
        "rec": "rec",
        "sit": "sit",
        "descripcion": "descripcion",
        "apr._inicial": "apr_inicial",
        "apr._adicionada": "apr_adicionada",
        "apr._reducida": "apr_reducida",
        "apr._vigente": "apr_vigente",
        "apr_bloqueada": "apr_bloqueada",
        "cdp": "cdp",
        "apr._disponible": "apr_disponible",
        "compromiso": "compromiso",
        "orden_pago": "orden_pago",
        "pagos": "pagos",
        "fecha": "fecha",
    }

    # Única fuente de verdad para la regla de agregación
    NON_AGGREGATED_SHEETS = {"ejecuciondesagregada-minc"}

    sheets: dict[str, str] = {
        "inm": "INM",
        "mincit": "MINCIT",
        "jcc": "JCC",
        "supersociedades": "SUPERSOC",
        "superindustria": "SIC",
        "ejecuciondesagregada-minc": "MINCIT",
    }

    def __init__(self, sheet_name: str | None = None):
        super().__init__(destination_table="ejecucion_presupuestal_p")
        self._es_agregada: int = 0 if sheet_name in self.NON_AGGREGATED_SHEETS else 1
        self._entity = self.sheets.get(sheet_name) if sheet_name else None


    def _transform(self, df):
        df = df.filter(
            pl.col("uej").is_not_null()
            & pl.col("rubro").is_not_null()
            & pl.col("rec").is_not_null()
            & pl.col("fecha").is_not_null()
        )

        if self._entity:
            df = df.with_columns(pl.lit(self._entity).alias("entidad"))

        # Se inyecta valor agregada
        df = df.with_columns(pl.lit(self._es_agregada).cast(pl.Int8).alias("es_agregada"))

        return df
