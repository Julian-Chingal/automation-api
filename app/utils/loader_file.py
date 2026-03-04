from core.exceptions import UnsupportedFileFormatError, FileReadError, FileReadSheetsError
from fastapi import UploadFile
import polars as pl
import unicodedata
import openpyxl
import io

SUPPORTED_EXTENSIONS = {
    "csv": pl.read_csv,
    "xlsx": pl.read_excel,
    "xls": pl.read_excel,
    "xlsb": pl.read_excel,
}


def normalize_sheet_name(name: str) -> str:
    """Normaliza nombres de hojas: elimina espacios y acentos."""
    # Eliminar espacios en blanco
    name = name.strip().replace(" ", "")
    
    # Eliminar acentos y tildes
    nfkd_form = unicodedata.normalize("NFKD", name)
    normalized = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    
    return normalized.lower()

async def load_file(file: UploadFile) -> pl.DataFrame:
    extension = file.filename.rsplit(".", 1)[-1].lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise UnsupportedFileFormatError(extension, list(SUPPORTED_EXTENSIONS.keys()))

    content = await file.read()
    reader = SUPPORTED_EXTENSIONS[extension]

    try:
        return reader(io.BytesIO(content))
    except Exception as e:
        raise FileReadError(file.filename, {"original_error": str(e)}) from e
    

async def load_all_sheets(
        file: UploadFile,
        sheets: set[str],
        skip_rows: int = 0,
    ) -> dict[str, pl.DataFrame]:
    
    extension = file.filename.rsplit(".",1)[-1].lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise UnsupportedFileFormatError(extension, list(SUPPORTED_EXTENSIONS.keys()))

    content = await file.read()
    buffer = io.BytesIO(content)

    try:
        wb = openpyxl.load_workbook(buffer, read_only=True, data_only=True)
        available_sheets = set(wb.sheetnames)
        wb.close()
        buffer.seek(0)
    except Exception as e:
        raise FileReadError(file.filename, {"original_error": str(e)}) from e
    
    #! Normalizar nombres de hojas disponibles y crear mapeo
    normalized_to_original = {normalize_sheet_name(name): name for name in available_sheets}
    normalized_requested = {normalize_sheet_name(name) for name in sheets}
    
    #! Validación de hojas
    matched = normalized_requested & set(normalized_to_original.keys())
    missing = normalized_requested - matched

    if missing:
        raise FileReadSheetsError(extension, {"original_error": f"Hojas no encontradas en el archivo '%s': %s: {missing}"})
    
    if not matched:
        raise FileReadError(
            file.filename,
            {"original_error": f"Ninguna hoja esperada existe. Disponibles: {list(available_sheets)}"},
        )
    
    result: dict[str, pl.DataFrame] = {}
    for norm_name in matched:
        original_name = normalized_to_original[norm_name]
        try:
            df = pl.read_excel(
                buffer, 
                sheet_name=original_name, 
                has_header=False
            )
            
            # Salto lineas inciales
            df = df.slice(skip_rows)
            header = df.row(0)
            header = [str(col).strip().lower() for col in header]
            df = df.slice(1).rename(dict(zip(df.columns, header)))
            
            result[original_name] = df
            buffer.seek(0)
        
        except Exception as e:
            raise FileExistsError(
                extension,
                 {"original_error": f"Error leyendo hoja '{original_name}': {str(e)}"},
            )
        
    return result