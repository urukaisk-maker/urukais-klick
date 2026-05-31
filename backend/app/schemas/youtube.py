"""
Esquemas para YouTube API
"""

from pydantic import BaseModel
from typing import Optional

class YouTubeVideo(BaseModel):
    video_id: str
    title: str
    description: str
    thumbnail: str
    channel_title: str
    duration: Optional[str] = None
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    published_at: Optional[str] = None

class YouTubeSearchRequest(BaseModel):
    query: str
    max_results: int = 10
