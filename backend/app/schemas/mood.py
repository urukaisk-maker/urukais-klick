"""
Esquemas de estados de ánimo
"""

from pydantic import BaseModel
from typing import List, Optional

class MoodSelection(BaseModel):
    moods: List[str]
    
class MoodProfile(BaseModel):
    primary_mood: str
    secondary_moods: List[str]
    musical_preferences: List[str]
