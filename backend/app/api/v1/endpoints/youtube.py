"""
Endpoints para integración con YouTube API
"""

from fastapi import APIRouter, Depends, HTTPException
from app.schemas.youtube import YouTubeVideo, YouTubeSearchRequest
from app.services.youtube import youtube_service

router = APIRouter()

@router.post("/search", response_model=list[YouTubeVideo])
async def search_youtube_music(request: YouTubeSearchRequest):
    """Buscar música en YouTube"""
    results = youtube_service.search_music(request.query, request.max_results)
    
    if not results:
        return []
    
    # Obtener detalles adicionales para cada video
    detailed_results = []
    for result in results:
        video_id = result['video_id']
        details = youtube_service.get_video_details(video_id)
        
        if details:
            detailed_results.append(YouTubeVideo(
                video_id=details['video_id'],
                title=details['title'],
                description=details['description'],
                thumbnail=details['thumbnail'],
                channel_title=details['channel_title'],
                duration=details['duration'],
                view_count=details['view_count'],
                like_count=details['like_count'],
                published_at=details['published_at']
            ))
        else:
            detailed_results.append(YouTubeVideo(
                video_id=result['video_id'],
                title=result['title'],
                description=result['description'],
                thumbnail=result['thumbnail'],
                channel_title=result['channel_title']
            ))
    
    return detailed_results

@router.get("/video/{video_id}", response_model=YouTubeVideo)
async def get_youtube_video_details(video_id: str):
    """Obtener detalles de un video de YouTube"""
    details = youtube_service.get_video_details(video_id)
    
    if not details:
        raise HTTPException(status_code=404, detail="Video no encontrado")
    
    return YouTubeVideo(
        video_id=details['video_id'],
        title=details['title'],
        description=details['description'],
        thumbnail=details['thumbnail'],
        channel_title=details['channel_title'],
        duration=details['duration'],
        view_count=details['view_count'],
        like_count=details['like_count'],
        published_at=details['published_at']
    )
