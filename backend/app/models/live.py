"""
Modelos para salas de escucha en directo (LiveKlick)
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class LiveRoom(Base):
    __tablename__ = "live_rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    host_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    stream_url = Column(String(512), nullable=True)  # URL del stream WebRTC
    max_listeners = Column(Integer, default=1000)  # Sin límite por defecto
    current_listeners = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)
    
    host = relationship("User", backref="hosted_rooms")

class LiveChatMessage(Base):
    __tablename__ = "live_chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("live_rooms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    message_type = Column(String(20), default="text")  # "text", "reaction", "klick"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    room = relationship("LiveRoom", backref="chat_messages")
    user = relationship("User", backref="chat_messages")

class LiveReaction(Base):
    __tablename__ = "live_reactions"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("live_rooms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reaction_type = Column(String(20), nullable=False)  # "👏", "❤️", "🔥", etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    room = relationship("LiveRoom", backref="reactions")
    user = relationship("User", backref="live_reactions")
