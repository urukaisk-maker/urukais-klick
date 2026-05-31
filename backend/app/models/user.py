"""
Modelo de usuario
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    alias = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)  # Opcional para acceso anónimo
    is_artist = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Perfil de oyente
    mood_profile = Column(Text)  # JSON con estados de ánimo
    
    # Perfil de artista
    artist_bio = Column(Text, nullable=True)
    artist_links = Column(Text, nullable=True)  # JSON con enlaces a redes
