"""
Whisper transkripsiyon servisi
"""
import os
import warnings
import whisper
import pandas as pd
from typing import List, Dict
from ..config import WHISPER_MODEL_SIZE

# Debug klasörü ve dosya yolu
DEBUG_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "debug_output")
TRANSCRIPT_CSV_PATH = os.path.join(DEBUG_OUTPUT_DIR, "transcript.csv")


def _ensure_debug_dir():
    """Debug klasörünü oluştur (yoksa)"""
    os.makedirs(DEBUG_OUTPUT_DIR, exist_ok=True)


class TranscriptionService:
    """Whisper ile ses transkripsiyon işlemleri"""
    
    def __init__(self, model_size: str = WHISPER_MODEL_SIZE):
        self._model_size = model_size
        self._model = None
    
    def _load_model(self):
        """Whisper modelini lazy loading ile yükle"""
        if self._model is None:
            print(f"[TranscriptionService] Whisper modeli yükleniyor: {self._model_size}...")
            self._model = whisper.load_model(self._model_size)
        return self._model
    
    def transcribe(self, audio_path: str, delete_after: bool = True) -> List[Dict]:
        """
        Ses dosyasını transkribe et.
        
        Args:
            audio_path: Ses dosyasının yolu
            delete_after: İşlem sonrası dosyayı sil
            
        Returns:
            Segment listesi [{"start": float, "end": float, "text": str}, ...]
        """
        print("[TranscriptionService] Transkripsiyon başlatılıyor...")
        
        model = self._load_model()
        
        # FP16 uyarısını bastır (CPU'da beklenen davranış)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")
            result = model.transcribe(audio_path)
        
        segments = [
            {
                "start": round(seg['start'], 2),
                "end": round(seg['end'], 2),
                "text": seg['text'].strip()
            }
            for seg in result['segments']
        ]
        
        # CSV'ye kaydet (debug için) - her seferinde üzerine yazar
        _ensure_debug_dir()
        df = pd.DataFrame(segments)
        df.to_csv(TRANSCRIPT_CSV_PATH, index=False)
        print(f"[TranscriptionService] CSV kaydedildi: debug_output/transcript.csv")
        
        print(f"[TranscriptionService] Transkripsiyon tamamlandı. {len(segments)} segment bulundu.")
        
        # Ses dosyasını sil
        if delete_after and os.path.exists(audio_path):
            os.remove(audio_path)
        
        return segments


# Singleton instance
transcription_service = TranscriptionService()

