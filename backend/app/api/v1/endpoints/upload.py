"""
Endpoints para subida de archivos
"""

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.services.storage import storage_service
from app.schemas.upload import UploadResponse

router = APIRouter()

@router.post("/audio", response_model=UploadResponse)
async def upload_audio(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Subir archivo de audio"""
    if not current_user.is_artist:
        raise HTTPException(
            status_code=403,
            detail="Solo los artistas pueden subir archivos de audio"
        )
    
    url = await storage_service.upload_audio_file(file, current_user.id)
    
    return UploadResponse(
        url=url,
        message="Archivo subido exitosamente"
    )

@router.post("/cover", response_model=UploadResponse)
async def upload_cover(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Subir imagen de portada"""
    if not current_user.is_artist:
        raise HTTPException(
            status_code=403,
            detail="Solo los artistas pueden subir imágenes de portada"
        )
    
    url = await storage_service.upload_cover_image(file, current_user.id)
    
    return UploadResponse(
        url=url,
        message="Imagen subida exitosamente"
    )
