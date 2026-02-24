from .base_transformer import BaseTransformer
from core.db_manager import DBManager
from sqlalchemy import text
import polars as pl

def upload_dataframe(
        df: pl.DataFrame,
        transformer: BaseTransformer,
        db_manager: DBManager,
        db_alias: str,
) -> int:
    """
    Transforms and uploads a DataFrame to the database.
    """
    transformed = transformer.transform(df)
    engine = db_manager.get_engine(db_alias)

    if transformed.is_empty():
        return 0
    
    rows = transformed.to_dicts()
    colunms = transformed.columns
    column_list = ", ".join(colunms)
    placeholders = ", ".join([f":{col}" for col in colunms])

    sql = text(f"""
        INSERT IGNORE INTO {transformer.destination_table}
        ({column_list})
        VALUES ({placeholders})
    """)

    with engine.begin() as conn:
        result = conn.execute(sql, rows)
        
    return result.rowcount