from pydantic import BaseModel

class UploadResponse(BaseModel):
    status: bool
    message: str
    rows_uploaded: int
    destination_table: str