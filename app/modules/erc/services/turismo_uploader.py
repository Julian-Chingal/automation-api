from ..transformers.turismo_transform import TurismoTransformer
from utils.uploader import upload_dataframe
from core.db_manager import DBManager
import polars as pl

def upload_turismo(df: pl.DataFrame, db_manager: DBManager, db_alias: str) -> int:
    return upload_dataframe(
        df,
        TurismoTransformer(),
        db_manager,
        db_alias
    )