"""
Video cache yönetimi servisi
"""
import time
import asyncio
from typing import Dict, List, Optional, Any
from ..config import CACHE_MAX_SIZE


class CacheService:
    """Video altyazıları için cache yönetimi"""
    
    def __init__(self, max_size: int = CACHE_MAX_SIZE):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._in_progress: Dict[str, asyncio.Future] = {}
        self._max_size = max_size
    
    def get(self, video_id: str) -> Optional[List[Dict]]:
        """
        Cache'den altyazıları getir.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Altyazı listesi veya None
        """
        if video_id in self._cache:
            return self._cache[video_id]["subtitles"]
        return None
    
    def set(self, video_id: str, subtitles: List[Dict]) -> None:
        """
        Altyazıları cache'e kaydet.
        
        Args:
            video_id: YouTube video ID
            subtitles: Altyazı listesi
        """
        self._cache[video_id] = {
            "subtitles": subtitles,
            "timestamp": time.time()
        }
        self._cleanup_if_needed()
    
    def _cleanup_if_needed(self) -> None:
        """Cache boyutu aşılırsa en eski kaydı sil"""
        if len(self._cache) > self._max_size:
            oldest = sorted(
                self._cache.items(), 
                key=lambda x: x[1]["timestamp"]
            )[0][0]
            del self._cache[oldest]
    
    def is_processing(self, video_id: str) -> bool:
        """Video şu an işleniyor mu?"""
        return video_id in self._in_progress
    
    def get_future(self, video_id: str) -> Optional[asyncio.Future]:
        """İşlemdeki video için future döndür"""
        return self._in_progress.get(video_id)
    
    def set_processing(self, video_id: str, future: asyncio.Future) -> None:
        """Video işleme başladığını işaretle"""
        self._in_progress[video_id] = future
    
    def clear_processing(self, video_id: str) -> None:
        """Video işleme tamamlandı"""
        if video_id in self._in_progress:
            del self._in_progress[video_id]


# Singleton instance
cache_service = CacheService()

