from .base_transformer import BaseTransformer
from core.db_manager import DBManager
from core.exceptions import DatabaseInsertError, DatabaseDeleteError
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

    try:
        with engine.begin() as conn:
            result = conn.execute(sql, rows)
    except Exception as e:
        raise DatabaseInsertError({
            "table": transformer.destination_table,
            "rows_attempted": len(rows),
            "error": str(e)
        }) from e
        
    return result.rowcount

def full_reload_dataframe(
    df: pl.DataFrame,
    transformer: BaseTransformer,
    db_manager: DBManager,
    db_alias: str
) -> int:

    engine = db_manager.get_engine(db_alias)

    transformed = transformer.transform(df)

    if transformed.is_empty():
        return 0

    rows = transformed.to_dicts()
    columns = transformed.columns
    column_list = ", ".join(columns)
    placeholders = ", ".join([f":{col}" for col in columns])

    delete_sql = text(f"DELETE FROM {transformer.destination_table}")

    insert_sql = text(f"""
        INSERT INTO {transformer.destination_table}
        ({column_list})
        VALUES ({placeholders})
    """)

    try:
        with engine.begin() as conn:
            conn.execute(delete_sql)
            result = conn.execute(insert_sql, rows)
    except Exception as e:
        raise DatabaseInsertError({
            "table": transformer.destination_table,
            "rows_attempted": len(rows),
            "error": str(e)
        }) from e

    return result.rowcount