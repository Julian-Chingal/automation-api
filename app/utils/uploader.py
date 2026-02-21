from .base_transformer import BaseTransformer
from core.db_manager import DBManager
import polars as pl

def upload_dataframe(
        df: pl.DataFrame,
        transformer: BaseTransformer,
        db_manager: DBManager,
        db_alias: str,
        if_table_exists: str = "append"
) -> int:
    """
    Transforms and uploads a DataFrame to the database.
    """
    transformed = transformer.transform(df)
    engine = db_manager.get_engine(db_alias)

    transformed.write_database(
        table_name=transformer.destination_table,
        connection=engine,
        if_table_exists=if_table_exists,
    )
    return len(transformed)