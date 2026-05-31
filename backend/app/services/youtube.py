"""
Servicio de integración con YouTube API
"""

from googleapiclient.discovery import build
from typing import List, Dict, Optional
from app.core.config import settings

class YouTubeService:
    def __init__(self):
        self.api_key = settings.YOUTUBE_API_KEY
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
    
    def search_music(
        self,
        query: str,
        max_results: int = 10
    ) -> List[Dict]:
        """
        Buscar música en YouTube
        """
        try:
            search_response = self.youtube.search().list(
                q=query,
                part='id,snippet',
                maxResults=max_results,
                type='video',
                videoCategoryId='10'  # Categoría de música
            ).execute()
            
            results = []
            for item in search_response.get('items', []):
                video_id = item['id']['videoId']
                snippet = item['snippet']
                
                results.append({
                    'video_id': video_id,
                    'title': snippet['title'],
                    'description': snippet.get('description', ''),
                    'thumbnail': snippet['thumbnails']['default']['url'],
                    'channel_title': snippet['channelTitle'],
                    'published_at': snippet['publishedAt']
                })
            
            return results
        except Exception as e:
            print(f"Error searching YouTube: {e}")
            return []
    
    def get_video_details(
        self,
        video_id: str
    ) -> Optional[Dict]:
        """
        Obtener detalles de un video específico
        """
        try:
            video_response = self.youtube.videos().list(
                part='contentDetails,snippet,statistics',
                id=video_id
            ).execute()
            
            if not video_response.get('items'):
                return None
            
            item = video_response['items'][0]
            snippet = item['snippet']
            content_details = item['contentDetails']
            statistics = item['statistics']
            
            return {
                'video_id': video_id,
                'title': snippet['title'],
                'description': snippet.get('description', ''),
                'thumbnail': snippet['thumbnails']['high']['url'],
                'channel_title': snippet['channelTitle'],
                'duration': content_details['duration'],
                'view_count': statistics.get('viewCount', 0),
                'like_count': statistics.get('likeCount', 0),
                'published_at': snippet['publishedAt']
            }
        except Exception as e:
            print(f"Error getting video details: {e}")
            return None
    
    def get_video_duration_seconds(self, duration: str) -> int:
        """
        Convertir duración de formato ISO 8601 (PT1H2M3S) a segundos
        """
        import re
        pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
        match = re.match(pattern, duration)
        
        if not match:
            return 0
        
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        
        return hours * 3600 + minutes * 60 + seconds

youtube_service = YouTubeService()
