"""
Endpoints para el motor de recomendaciones Klicks
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.track import Track
from app.schemas.track import Track
from app.services.recommendation import recommendation_service

router = APIRouter()

@router.get("/klicks", response_model=List[Track])
async def get_klick_recommendations(
    limit: int = 10,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener recomendaciones Klicks personalizadas"""
    recommendations = recommendation_service.get_klick_recommendations(
        current_user, db, limit
    )
    return recommendations

@router.get("/trending", response_model=List[Track])
async def get_trending_tracks(
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Obtener pistas trending por Klicks"""
    trending = recommendation_service.get_trending_tracks(db, limit)
    return trending

@router.get("/discovery", response_model=List[Track])
async def get_discovery_tracks(
    limit: int = 10,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener pistas para descubrimiento fuera de lo habitual"""
    discovery = recommendation_service.get_discovery_tracks(current_user, db, limit)
    return discovery

@router.post("/eco/{track_id}")
async def register_eco(
    track_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Registrar un Eco (escucha > 30 segundos)"""
    success = recommendation_service.register_eco(track_id, current_user, db)
    if success:
        return {"message": "Eco registrado exitosamente"}
    return {"message": "Error al registrar Eco"}
