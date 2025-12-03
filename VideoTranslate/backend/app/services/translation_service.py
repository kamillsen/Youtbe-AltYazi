"""
MarianMT çeviri servisi
"""
import os
import warnings
import torch
import pandas as pd
from typing import List
from transformers import MarianMTModel, MarianTokenizer
from nltk.tokenize import sent_tokenize
import nltk
from ..config import TRANSLATION_MODEL_NAME, NLTK_DATA_PACKAGES

# Gereksiz uyarıları bastır
warnings.filterwarnings("ignore", message=".*sacremoses.*")

# Debug klasörü ve dosya yolu
DEBUG_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "debug_output")
SUBTITLES_CSV_PATH = os.path.join(DEBUG_OUTPUT_DIR, "subtitles_with_translation.csv")


def _ensure_debug_dir():
    """Debug klasörünü oluştur (yoksa)"""
    os.makedirs(DEBUG_OUTPUT_DIR, exist_ok=True)


class TranslationService:
    """MarianMT ile İngilizce-Türkçe çeviri işlemleri"""
    
    def __init__(self, model_name: str = TRANSLATION_MODEL_NAME):
        self._model_name = model_name
        self._tokenizer = None
        self._model = None
        self._setup_nltk()
    
    def _setup_nltk(self):
        """NLTK veri paketlerini indir"""
        for package in NLTK_DATA_PACKAGES:
            try:
                nltk.download(package, quiet=True)
            except Exception:
                pass
    
    def _load_model(self):
        """Model ve tokenizer'ı lazy loading ile yükle"""
        if self._tokenizer is None:
            print(f"[TranslationService] Model yükleniyor: {self._model_name}...")
            self._tokenizer = MarianTokenizer.from_pretrained(self._model_name)
            self._model = MarianMTModel.from_pretrained(self._model_name)
        return self._tokenizer, self._model
    
    def translate_text(self, text: str) -> str:
        """
        Tek bir metni çevir.
        
        Args:
            text: Çevrilecek metin
            
        Returns:
            Çevrilmiş metin
        """
        try:
            tokenizer, model = self._load_model()
            inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
            with torch.no_grad():
                translated = model.generate(**inputs)
            return tokenizer.decode(translated[0], skip_special_tokens=True)
        except Exception:
            return "[Çeviri Hatası]"
    
    def translate_segments(self, segments: List[dict]) -> List[dict]:
        """
        Segment listesini çevir.
        
        Args:
            segments: [{"start": float, "end": float, "text": str}, ...]
            
        Returns:
            [{"start": float, "end": float, "text": str, "translation": str}, ...]
        """
        print(f"[TranslationService] {len(segments)} segment çeviriliyor...")
        
        for segment in segments:
            # Metni cümlelere ayır
            sentences = sent_tokenize(segment["text"])
            # Her cümleyi çevir
            translated_sentences = [self.translate_text(sent) for sent in sentences]
            # Birleştir
            segment["translation"] = " ".join(translated_sentences)
        
        # CSV'ye kaydet (debug için) - her seferinde üzerine yazar
        _ensure_debug_dir()
        df = pd.DataFrame(segments)
        df.to_csv(SUBTITLES_CSV_PATH, index=False)
        print(f"[TranslationService] CSV kaydedildi: debug_output/subtitles_with_translation.csv")
        
        print("[TranslationService] Çeviri tamamlandı.")
        return segments


# Singleton instance
translation_service = TranslationService()

