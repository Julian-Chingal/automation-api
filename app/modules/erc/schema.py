from pydantic import BaseModel

class UploadResponse(BaseModel):
    message: str
    rows_uploaded: int
    destination_table: str