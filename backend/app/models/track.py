"""
Modelo de pista musical
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Track(Base):
    __tablename__ = "tracks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    artist_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    duration = Column(Float)  # Duración en segundos
    audio_url = Column(String(512), nullable=False)
    cover_url = Column(String(512), nullable=True)
    genre_tags = Column(Text)  # JSON con etiquetas de género
    mood_tags = Column(Text)  # JSON con etiquetas de estado de ánimo
    play_count = Column(Integer, default=0)
    klick_count = Column(Integer, default=0)  # Contador de "Klicks de apoyo"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    artist = relationship("User", backref="tracks")
