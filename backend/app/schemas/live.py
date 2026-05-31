"""
Esquemas para salas de escucha en directo
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LiveRoomBase(BaseModel):
    title: str
    description: Optional[str] = None
    max_listeners: Optional[int] = 1000

class LiveRoomCreate(LiveRoomBase):
    pass

class LiveRoom(LiveRoomBase):
    id: int
    host_id: int
    is_active: bool
    stream_url: Optional[str] = None
    current_listeners: int
    created_at: datetime
    ended_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class LiveChatMessageBase(BaseModel):
    message: str
    message_type: str = "text"

class LiveChatMessageCreate(LiveChatMessageBase):
    room_id: int

class LiveChatMessage(LiveChatMessageBase):
    id: int
    room_id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class LiveReactionBase(BaseModel):
    reaction_type: str

class LiveReactionCreate(LiveReactionBase):
    room_id: int

class LiveReaction(LiveReactionBase):
    id: int
    room_id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
