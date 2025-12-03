"""
YouTube ses indirme servisi
"""
import os
import tempfile
import yt_dlp
from ..config import AUDIO_FORMAT, AUDIO_QUALITY


class YouTubeService:
    """YouTube'dan ses indirme işlemleri"""
    
    def __init__(self):
        self._ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,  # Uyarıları bastır
            'extractor_args': {
                'youtube': {
                    'player_client': ['default'],  # JS runtime uyarısını önle
                }
            },
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': AUDIO_FORMAT,
                'preferredquality': AUDIO_QUALITY,
            }],
        }
    
    def download_audio(self, video_url: str) -> str:
        """
        YouTube videosundan ses indir.
        
        Args:
            video_url: YouTube video URL'si
            
        Returns:
            İndirilen ses dosyasının yolu
            
        Raises:
            RuntimeError: Ses indirilemezse
        """
        print(f"[YouTubeService] Ses indiriliyor: {video_url}")
        
        # Geçici dosya oluştur
        with tempfile.NamedTemporaryFile(suffix=f".{AUDIO_FORMAT}", delete=False) as temp_audio:
            temp_path = temp_audio.name
        
        # yt-dlp ayarlarını güncelle
        opts = self._ydl_opts.copy()
        opts['outtmpl'] = temp_path.replace(f".{AUDIO_FORMAT}", ".%(ext)s")
        
        # İndir
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([video_url])
        
        # Dosya kontrolü
        downloaded_path = temp_path.replace(f".{AUDIO_FORMAT}", f".{AUDIO_FORMAT}")
        if not os.path.exists(downloaded_path):
            raise RuntimeError("Ses indirilemedi.")
        
        print(f"[YouTubeService] Ses dosyası: {downloaded_path}")
        return downloaded_path


# Singleton instance
youtube_service = YouTubeService()

