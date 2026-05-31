"""
Motor de recomendaciones Klicks - Descubrimiento musical basado en afinidad emocional
"""

import json
import random
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.track import Track
from app.core.database import get_db

class RecommendationService:
    def __init__(self):
        self.eco_threshold = 30  # Segundos para considerar un "Eco"
    
    def get_user_mood_profile(self, user: User) -> dict:
        """Obtener perfil de estado de ánimo del usuario"""
        if not user.mood_profile:
            return {"primary_mood": "relaxed", "musical_preferences": ["ambient", "lo-fi"]}
        return json.loads(user.mood_profile)
    
    def get_klick_recommendations(
        self,
        user: User,
        db: Session,
        limit: int = 10
    ) -> List[Track]:
        """
        Generar recomendaciones Klicks basadas en:
        - Afinidad emocional
        - Géneros musicales preferidos
        - Popularidad en la comunidad
        """
        mood_profile = self.get_user_mood_profile(user)
        preferred_genres = mood_profile.get("musical_preferences", [])
        
        # Construir consulta base
        query = db.query(Track)
        
        # Filtrar por géneros preferidos si existen
        if preferred_genres:
            # Buscar pistas que tengan etiquetas de género coincidentes
            genre_conditions = []
            for genre in preferred_genres:
                genre_conditions.append(Track.genre_tags.like(f"%{genre}%"))
            
            from sqlalchemy import or_
            query = query.filter(or_(*genre_conditions))
        
        # Ordenar por combinación de popularidad y aleatoriedad
        # Esto permite descubrimiento + popularidad
        tracks = query.order_by(Track.klick_count.desc()).limit(limit * 3).all()
        
        # Mezclar resultados para variabilidad
        random.shuffle(tracks)
        
        return tracks[:limit]
    
    def get_trending_tracks(
        self,
        db: Session,
        limit: int = 20
    ) -> List[Track]:
        """Obtener pistas trending por Klicks recientes"""
        return db.query(Track).order_by(Track.klick_count.desc()).limit(limit).all()
    
    def get_discovery_tracks(
        self,
        user: User,
        db: Session,
        limit: int = 10
    ) -> List[Track]:
        """
        Obtener pistas para descubrimiento puro
        - Fuera de los géneros habituales del usuario
        - Menos populares pero de calidad
        """
        mood_profile = self.get_user_mood_profile(user)
        preferred_genres = mood_profile.get("musical_preferences", [])
        
        # Obtener todas las pistas
        all_tracks = db.query(Track).all()
        
        # Filtrar pistas que NO están en los géneros preferidos
        discovery_tracks = []
        for track in all_tracks:
            if not track.genre_tags:
                discovery_tracks.append(track)
                continue
            
            track_genres = json.loads(track.genre_tags) if isinstance(track.genre_tags, str) else track.genre_tags
            if not any(genre in preferred_genres for genre in track_genres):
                discovery_tracks.append(track)
        
        # Mezclar y limitar
        random.shuffle(discovery_tracks)
        return discovery_tracks[:limit]
    
    def register_eco(
        self,
        track_id: int,
        user: User,
        db: Session
    ) -> bool:
        """
        Registrar un "Eco" - cuando un usuario escucha una pista más de 30 segundos
        Esto enriquece el perfil del usuario y la comunidad
        """
        track = db.query(Track).filter(Track.id == track_id).first()
        if not track:
            return False
        
        # Incrementar contador de reproducciones
        track.play_count += 1
        
        # Actualizar perfil del usuario con el eco
        mood_profile = self.get_user_mood_profile(user)
        recent_ecos = mood_profile.get("recent_ecos", [])
        
        eco_entry = {
            "track_id": track_id,
            "track_title": track.title,
            "artist_id": track.artist_id,
            "timestamp": "now"
        }
        
        recent_ecos.insert(0, eco_entry)
        if len(recent_ecos) > 50:  # Mantener solo los últimos 50 ecos
            recent_ecos = recent_ecos[:50]
        
        mood_profile["recent_ecos"] = recent_ecos
        user.mood_profile = json.dumps(mood_profile)
        
        db.commit()
        return True

recommendation_service = RecommendationService()
