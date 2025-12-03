"""
Yardımcı fonksiyonlar
"""
from urllib.parse import urlparse, parse_qs
from typing import Optional


def extract_video_id(url: str) -> Optional[str]:
    """
    YouTube URL'sinden video ID'sini çıkarır.
    
    Args:
        url: YouTube video URL'si
        
    Returns:
        Video ID veya None
        
    Example:
        >>> extract_video_id("https://www.youtube.com/watch?v=abc123")
        "abc123"
    """
    try:
        query = parse_qs(urlparse(url).query)
        return query.get("v", [None])[0]
    except Exception:
        return None

