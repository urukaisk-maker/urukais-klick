"""
Endpoints de pistas musicales
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.track import Track, TrackCreate, TrackUpdate
from app.models.track import Track as TrackModel

router = APIRouter()

@router.post("/", response_model=Track)
async def create_track(
    track: TrackCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Crear una nueva pista musical"""
    if not current_user.is_artist:
        raise HTTPException(
            status_code=403,
            detail="Solo los artistas pueden crear pistas"
        )
    
    new_track = TrackModel(
        title=track.title,
        artist_id=current_user.id,
        duration=track.duration,
        audio_url=track.audio_url,
        cover_url=track.cover_url,
        genre_tags=track.genre_tags,
        mood_tags=track.mood_tags
    )
    db.add(new_track)
    db.commit()
    db.refresh(new_track)
    return new_track

@router.get("/{track_id}", response_model=Track)
async def get_track(track_id: int, db: Session = Depends(get_db)):
    """Obtener una pista por ID"""
    track = db.query(TrackModel).filter(TrackModel.id == track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Pista no encontrada")
    return track

@router.get("/", response_model=List[Track])
async def get_tracks(
    skip: int = 0,
    limit: int = 100,
    artist_id: int = None,
    db: Session = Depends(get_db)
):
    """Obtener lista de pistas"""
    query = db.query(TrackModel)
    
    if artist_id:
        query = query.filter(TrackModel.artist_id == artist_id)
    
    tracks = query.order_by(TrackModel.created_at.desc()).offset(skip).limit(limit).all()
    return tracks

@router.post("/{track_id}/klick")
async def klick_track(
    track_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Enviar un Klick de apoyo a una pista"""
    track = db.query(TrackModel).filter(TrackModel.id == track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Pista no encontrada")
    
    track.klick_count += 1
    db.commit()
    db.refresh(track)
    
    return {
        "message": "Klick enviado",
        "klick_count": track.klick_count,
        "track_title": track.title,
        "artist_id": track.artist_id
    }
