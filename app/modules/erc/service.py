from .transformers import (
    TurismoTransformer,
    InversionTransformer,
    ServiciosTransformer,
    BienesTransformer
)
from utils.uploader import upload_dataframe
from core.db_manager import DBManager
import polars as pl

ALIAS = "erc"

def turismo_service(df: pl.DataFrame, db_manager: DBManager) -> int:
    return upload_dataframe(
        df,
        TurismoTransformer(),
        db_manager,
        ALIAS
    )

def inversion_service(df: pl.DataFrame, db_manager: DBManager) -> int:
    return upload_dataframe(
        df,
        InversionTransformer(),
        db_manager,
        ALIAS
    )

def servicios_service(df: pl.DataFrame, db_manager: DBManager) -> int:
    return upload_dataframe(
        df,
        ServiciosTransformer(),
        db_manager,
        ALIAS
    )

def bienes_service(df: pl.DataFrame, db_manager: DBManager) -> int:
    return upload_dataframe(
        df,
        BienesTransformer(),
        db_manager,
        ALIAS
    )