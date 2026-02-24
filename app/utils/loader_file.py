from fastapi import UploadFile
import polars as pl
import io
from core.exceptions import UnsupportedFileFormatError, FileReadError

SUPPORTED_EXTENSIONS = {
    "csv": pl.read_csv,
    "xlsx": pl.read_excel,
    "xls": pl.read_excel,
    "xlsb": pl.read_excel,
}

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