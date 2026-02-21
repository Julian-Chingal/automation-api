import polars as pl
from fastapi import UploadFile
import io

SUPPORTED_EXTENSIONS = {
    "csv": pl.read_csv,
    "xlsx": pl.read_excel,
    "xls": pl.read_excel,
}

async def load_file(file: UploadFile) -> pl.DataFrame:
    extension = file.filename.rsplit(".", 1)[-1].lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Formato no soportado: '.{extension}'. Soportados: {list(SUPPORTED_EXTENSIONS)}")

    content = await file.read()
    reader = SUPPORTED_EXTENSIONS[extension]

    try:
        return reader(io.BytesIO(content))
    except Exception as e:
        raise RuntimeError(f"Error al leer el archivo '{file.filename}': {e}") from e