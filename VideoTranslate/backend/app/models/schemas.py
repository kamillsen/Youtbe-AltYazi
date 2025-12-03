"""
Pydantic modelleri - API request/response şemaları
"""
from pydantic import BaseModel
from typing import List, Optional


class URLPayload(BaseModel):
    """Video URL'si için request modeli"""
    url: str


class SubtitleItem(BaseModel):
    """Tek bir altyazı segmenti"""
    start: float
    end: float
    text: str
    translation: str


class SubtitleResponse(BaseModel):
    """Altyazı response modeli"""
    success: bool
    cached: bool = False
    subtitles: Optional[List[SubtitleItem]] = None
    error: Optional[str] = None

