"""
Esquemas de pista musical para validación y serialización
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TrackBase(BaseModel):
    title: str
    duration: Optional[float] = None

class TrackCreate(TrackBase):
    audio_url: str
    cover_url: Optional[str] = None
    genre_tags: Optional[str] = None
    mood_tags: Optional[str] = None

class TrackUpdate(BaseModel):
    title: Optional[str] = None
    cover_url: Optional[str] = None
    genre_tags: Optional[str] = None
    mood_tags: Optional[str] = None

class TrackInDB(TrackBase):
    id: int
    artist_id: int
    audio_url: str
    cover_url: Optional[str] = None
    genre_tags: Optional[str] = None
    mood_tags: Optional[str] = None
    play_count: int
    klick_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class Track(TrackInDB):
    pass
