from .transform import EjecucionPresupuestalTransformer
from utils.uploader import upload_dataframe
from core.db_manager import DBManager
import polars as pl
from utils.loader_file import load_all_sheets
from fastapi import UploadFile


ALIAS = "ejecucion_presupuestal"  

async def ejecucion_presupuestal_service(
        file: UploadFile, 
        db_manager: DBManager
    ) -> dict[str, int]:

    sheets_data = await load_all_sheets(
        file= file, 
        sheets= set(EjecucionPresupuestalTransformer.sheets.keys()), 
        skip_rows= 3
    )
    
    results: dict[str, int] = {}

    for sheet_name, df in sheets_data.items():
        transformer = EjecucionPresupuestalTransformer(sheet_name=sheet_name)
        rows = upload_dataframe(df, transformer, db_manager, ALIAS)
        results[sheet_name] = rows

    return results
    