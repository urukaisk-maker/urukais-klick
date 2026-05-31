"""
Servicio de streaming con caché inteligente
"""

import redis
import json
from typing import Optional, List
from app.core.config import settings

class StreamingService:
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL)
        self.cache_ttl = 86400  # 24 horas en segundos
    
    async def cache_track_metadata(
        self,
        track_id: int,
        metadata: dict
    ) -> bool:
        """Cachear metadatos de una pista"""
        try:
            key = f"track:metadata:{track_id}"
            self.redis_client.setex(
                key,
                self.cache_ttl,
                json.dumps(metadata)
            )
            return True
        except Exception:
            return False
    
    async def get_cached_track_metadata(
        self,
        track_id: int
    ) -> Optional[dict]:
        """Obtener metadatos cacheados de una pista"""
        try:
            key = f"track:metadata:{track_id}"
            cached_data = self.redis_client.get(key)
            if cached_data:
                return json.loads(cached_data)
            return None
        except Exception:
            return None
    
    async def cache_user_recent_tracks(
        self,
        user_id: int,
        track_ids: List[int]
    ) -> bool:
        """Cachear pistas recientes del usuario para escucha offline"""
        try:
            key = f"user:recent:{user_id}"
            self.redis_client.setex(
                key,
                self.cache_ttl * 7,  # 7 días
                json.dumps(track_ids)
            )
            return True
        except Exception:
            return False
    
    async def get_user_recent_tracks(
        self,
        user_id: int
    ) -> List[int]:
        """Obtener pistas recientes del usuario"""
        try:
            key = f"user:recent:{user_id}"
            cached_data = self.redis_client.get(key)
            if cached_data:
                return json.loads(cached_data)
            return []
        except Exception:
            return []
    
    async def add_to_user_cache(
        self,
        user_id: int,
        track_id: int
    ) -> bool:
        """Agregar pista al caché del usuario"""
        recent_tracks = await self.get_user_recent_tracks(user_id)
        
        # Evitar duplicados y mantener máximo 50 pistas
        if track_id in recent_tracks:
            recent_tracks.remove(track_id)
        recent_tracks.insert(0, track_id)
        
        if len(recent_tracks) > 50:
            recent_tracks = recent_tracks[:50]
        
        return await self.cache_user_recent_tracks(user_id, recent_tracks)
    
    async def increment_play_count(
        self,
        track_id: int
    ) -> bool:
        """Incrementar contador de reproducciones en caché"""
        try:
            key = f"track:plays:{track_id}"
            self.redis_client.incr(key)
            self.redis_client.expire(key, self.cache_ttl)
            return True
        except Exception:
            return False
    
    async def get_cached_play_count(
        self,
        track_id: int
    ) -> int:
        """Obtener contador de reproducciones cacheado"""
        try:
            key = f"track:plays:{track_id}"
            count = self.redis_client.get(key)
            return int(count) if count else 0
        except Exception:
            return 0
    
    async def invalidate_track_cache(
        self,
        track_id: int
    ) -> bool:
        """Invalidar caché de una pista específica"""
        try:
            keys = [
                f"track:metadata:{track_id}",
                f"track:plays:{track_id}"
            ]
            self.redis_client.delete(*keys)
            return True
        except Exception:
            return False

streaming_service = StreamingService()
