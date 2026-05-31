"""
Esquemas para el muro social
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SocialPostBase(BaseModel):
    content: str
    track_id: Optional[int] = None
    mood: Optional[str] = None

class SocialPostCreate(SocialPostBase):
    pass

class SocialPost(SocialPostBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class SocialReactionBase(BaseModel):
    reaction_type: str
    track_response_id: Optional[int] = None

class SocialReactionCreate(SocialReactionBase):
    post_id: int

class SocialReaction(SocialReactionBase):
    id: int
    post_id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
