"""
Altyazı API endpoint'leri
"""
import asyncio
import time
import pandas as pd
from fastapi import APIRouter

from ..models.schemas import URLPayload, SubtitleResponse
from ..utils.helpers import extract_video_id
from ..services.cache_service import cache_service
from ..services.youtube_service import youtube_service
from ..services.transcription_service import transcription_service
from ..services.translation_service import translation_service

# Çeviri sonrası CSV dosyası
SUBTITLES_CSV_PATH = "subtitles_with_translation.csv"


router = APIRouter(tags=["subtitles"])


def process_video_sync(url: str) -> list:
    """
    Video işleme - senkron (executor'da çalışacak)
    
    Args:
        url: YouTube video URL'si
        
    Returns:
        Altyazı listesi
    """
    print(f"[Router] Video işleniyor: {url}")
    start_time = time.time()
    
    # 1. Ses indir
    audio_path = youtube_service.download_audio(url)
    
    # 2. Transkribe et
    segments = transcription_service.transcribe(audio_path)
    
    # 3. Çevir
    subtitles = translation_service.translate_segments(segments)
    
    # CSV'ye kaydet (çeviri dahil)
    df = pd.DataFrame(subtitles)
    df.to_csv(SUBTITLES_CSV_PATH, index=False)
    print(f"[Router] CSV kaydedildi: {SUBTITLES_CSV_PATH}")
    
    duration = round(time.time() - start_time, 2)
    print(f"[Router] İşlem tamamlandı. Süre: {duration} sn")
    
    return subtitles


@router.post("/send_url", response_model=SubtitleResponse)
async def receive_url(payload: URLPayload):
    """
    YouTube video URL'sinden altyazı üret.
    
    - Video ID çıkar
    - Cache kontrol et
    - Yoksa: ses indir → transkribe et → çevir
    - Cache'e kaydet ve döndür
    """
    # Video ID çıkar
    video_id = extract_video_id(payload.url)
    if not video_id:
        return SubtitleResponse(
            success=False, 
            error="Geçerli bir video ID alınamadı."
        )
    
    # Cache kontrol
    cached_subtitles = cache_service.get(video_id)
    if cached_subtitles:
        print(f"[Router] Cache'den döndürülüyor: {video_id}")
        return SubtitleResponse(
            success=True, 
            cached=True, 
            subtitles=cached_subtitles
        )
    
    # Zaten işleniyor mu?
    if cache_service.is_processing(video_id):
        print(f"[Router] Video zaten işleniyor, bekleniyor: {video_id}")
        future = cache_service.get_future(video_id)
        if future:
            await future
            return SubtitleResponse(
                success=True, 
                cached=True, 
                subtitles=cache_service.get(video_id)
            )
    
    # Yeni işleme başla
    loop = asyncio.get_event_loop()
    future = loop.create_future()
    cache_service.set_processing(video_id, future)
    
    try:
        # Executor'da çalıştır (blocking işlemler)
        subtitles = await loop.run_in_executor(
            None, 
            process_video_sync, 
            payload.url
        )
        
        # Cache'e kaydet
        cache_service.set(video_id, subtitles)
        
        # Future'ı tamamla
        future.set_result(True)
        cache_service.clear_processing(video_id)
        
        return SubtitleResponse(
            success=True, 
            cached=False, 
            subtitles=subtitles
        )
        
    except Exception as e:
        future.set_exception(e)
        cache_service.clear_processing(video_id)
        print(f"[Router] Hata: {e}")
        return SubtitleResponse(
            success=False, 
            error=str(e)
        )

