"""
Uygulama yapılandırma ayarları
"""
from typing import List

# ==================== MODEL AYARLARI ====================
TRANSLATION_MODEL_NAME: str = "Helsinki-NLP/opus-tatoeba-en-tr"
WHISPER_MODEL_SIZE: str = "base"

# ==================== CACHE AYARLARI ====================
CACHE_MAX_SIZE: int = 4  # Maksimum cache'de tutulacak video sayısı

# ==================== CORS AYARLARI ====================
CORS_ORIGINS: List[str] = ["*"]
CORS_ALLOW_CREDENTIALS: bool = True
CORS_ALLOW_METHODS: List[str] = ["*"]
CORS_ALLOW_HEADERS: List[str] = ["*"]

# ==================== AUDIO AYARLARI ====================
AUDIO_FORMAT: str = "wav"
AUDIO_QUALITY: str = "192"

# ==================== NLTK AYARLARI ====================
NLTK_DATA_PACKAGES: List[str] = ["punkt", "punkt_tab"]

