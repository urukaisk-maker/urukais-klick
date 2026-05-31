"""
Endpoints para gestión de estados de ánimo (ruleta de estados)
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.mood import MoodSelection, MoodProfile
import json

router = APIRouter()

# Lista de estados de ánimo disponibles para la ruleta
MOOD_OPTIONS = [
    {"id": "happy", "name": "Feliz", "emoji": "😊", "genres": ["pop", "reggaeton", "electronic"]},
    {"id": "sad", "name": "Triste", "emoji": "😢", "genres": ["ballad", "indie", "acoustic"]},
    {"id": "energetic", "name": "Energético", "emoji": "⚡", "genres": ["rock", "hip-hop", "edm"]},
    {"id": "relaxed", "name": "Relajado", "emoji": "😌", "genres": ["ambient", "lo-fi", "jazz"]},
    {"id": "romantic", "name": "Romántico", "emoji": "💕", "genres": ["r&b", "soul", "latin"]},
    {"id": "focused", "name": "Concentrado", "emoji": "🎯", "genres": ["classical", "instrumental", "ambient"]},
    {"id": "nostalgic", "name": "Nostálgico", "emoji": "📻", "genres": ["retro", "80s", "90s"]},
    {"id": "adventurous", "name": "Aventurero", "emoji": "🌍", "genres": ["world", "experimental", "fusion"]},
]

@router.get("/options")
async def get_mood_options():
    """Obtener opciones de estados de ánimo para la ruleta"""
    return MOOD_OPTIONS

@router.post("/select", response_model=MoodProfile)
async def select_moods(
    mood_selection: MoodSelection,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Guardar selección de estados de ánimo del usuario"""
    # Determinar estado de ánimo principal
    primary_mood = mood_selection.moods[0] if mood_selection.moods else "relaxed"
    
    # Obtener géneros musicales asociados
    selected_mood_data = next((m for m in MOOD_OPTIONS if m["id"] == primary_mood), MOOD_OPTIONS[3])
    musical_preferences = selected_mood_data["genres"]
    
    # Crear perfil de estado de ánimo
    mood_profile = {
        "primary_mood": primary_mood,
        "secondary_moods": mood_selection.moods[1:],
        "musical_preferences": musical_preferences,
        "updated_at": "now"
    }
    
    # Guardar en el usuario
    current_user.mood_profile = json.dumps(mood_profile)
    db.commit()
    
    return MoodProfile(
        primary_mood=primary_mood,
        secondary_moods=mood_selection.moods[1:],
        musical_preferences=musical_preferences
    )

@router.get("/profile")
async def get_mood_profile(
    current_user: User = Depends(get_current_active_user)
):
    """Obtener perfil de estado de ánimo del usuario"""
    if not current_user.mood_profile:
        return {"message": "Perfil no configurado"}
    
    return json.loads(current_user.mood_profile)
