"""
Modelos para el muro social
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class SocialPost(Base):
    __tablename__ = "social_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)  # "¿Qué estás sintiendo ahora?"
    track_id = Column(Integer, ForeignKey("tracks.id"), nullable=True)  # Fragmento de canción
    mood = Column(String(50), nullable=True)  # Estado de ánimo asociado
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", backref="social_posts")
    track = relationship("Track", backref="social_posts")

class SocialReaction(Base):
    __tablename__ = "social_reactions"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("social_posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reaction_type = Column(String(20), nullable=False)  # "klick", "heart", etc.
    track_response_id = Column(Integer, ForeignKey("tracks.id"), nullable=True)  # Responder con otro Klick
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    post = relationship("SocialPost", backref="reactions")
    user = relationship("User", backref="social_reactions")
    track_response = relationship("Track", backref="social_reactions")
