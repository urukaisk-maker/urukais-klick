"""
Endpoints para streaming y caché
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.track import Track
from app.services.streaming import streaming_service

router = APIRouter()

@router.get("/track/{track_id}/metadata")
async def get_track_metadata_with_cache(
    track_id: int,
    db: Session = Depends(get_db)
):
    """Obtener metadatos de pista con caché"""
    # Intentar obtener del caché
    cached_metadata = await streaming_service.get_cached_track_metadata(track_id)
    if cached_metadata:
        return {"source": "cache", "data": cached_metadata}
    
    # Obtener de la base de datos
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Pista no encontrada")
    
    metadata = {
        "id": track.id,
        "title": track.title,
        "artist_id": track.artist_id,
        "duration": track.duration,
        "audio_url": track.audio_url,
        "cover_url": track.cover_url,
        "play_count": track.play_count,
        "klick_count": track.klick_count
    }
    
    # Cachear para futuras consultas
    await streaming_service.cache_track_metadata(track_id, metadata)
    
    return {"source": "database", "data": metadata}

@router.post("/track/{track_id}/play")
async def register_play(
    track_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Registrar reproducción y actualizar caché"""
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Pista no encontrada")
    
    # Incrementar contador en base de datos
    track.play_count += 1
    db.commit()
    
    # Actualizar caché
    await streaming_service.increment_play_count(track_id)
    await streaming_service.add_to_user_cache(current_user.id, track_id)
    
    return {"message": "Reproducción registrada", "play_count": track.play_count}

@router.get("/my/recent")
async def get_my_recent_tracks(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener pistas recientes del usuario (para escucha offline)"""
    recent_track_ids = await streaming_service.get_user_recent_tracks(current_user.id)
    
    if not recent_track_ids:
        return {"tracks": []}
    
    # Obtener detalles de las pistas
    tracks = db.query(Track).filter(Track.id.in_(recent_track_ids)).all()
    
    # Ordenar según el orden del caché
    tracks_dict = {track.id: track for track in tracks}
    ordered_tracks = [tracks_dict[tid] for tid in recent_track_ids if tid in tracks_dict]
    
    return {
        "tracks": [
            {
                "id": track.id,
                "title": track.title,
                "artist_id": track.artist_id,
                "audio_url": track.audio_url,
                "cover_url": track.cover_url,
                "duration": track.duration
            }
            for track in ordered_tracks
        ]
    }
