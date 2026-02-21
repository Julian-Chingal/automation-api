from ..transformers.turismo_transform import TurismoTransformer
from utils.uploader import upload_dataframe
from core.db_manager import DBManager
import polars as pl

ALIAS = "erc"

def upload_turismo(df: pl.DataFrame, db_manager: DBManager) -> int:
    return upload_dataframe(
        df,
        TurismoTransformer(),
        db_manager,
        ALIAS
    )