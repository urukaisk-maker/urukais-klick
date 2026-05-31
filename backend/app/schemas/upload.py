"""
Esquemas para subida de archivos
"""

from pydantic import BaseModel

class UploadResponse(BaseModel):
    url: str
    message: str
