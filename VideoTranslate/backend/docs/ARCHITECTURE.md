# Mimari

## Proje Yapısı

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app, CORS, router bağlama
│   ├── config.py            # Tüm yapılandırma ayarları
│   │
│   ├── models/
│   │   └── schemas.py       # Pydantic request/response modelleri
│   │
│   ├── services/
│   │   ├── cache_service.py         # Video cache yönetimi
│   │   ├── youtube_service.py       # yt-dlp ile ses indirme
│   │   ├── transcription_service.py # Whisper transkripsiyon
│   │   └── translation_service.py   # MarianMT çeviri
│   │
│   ├── routers/
│   │   └── subtitle_router.py       # /send_url endpoint
│   │
│   └── utils/
│       └── helpers.py               # Yardımcı fonksiyonlar
│
├── docs/                    # Dokümantasyon
├── requirements.txt         # Bağımlılıklar
└── run.py                   # Başlatma scripti
```

## Veri Akışı

```
1. Request gelir (/send_url)
        ↓
2. Video ID çıkarılır (helpers.py)
        ↓
3. Cache kontrol edilir (cache_service.py)
        ↓ (cache miss)
4. YouTube'dan ses indirilir (youtube_service.py)
        ↓
5. Whisper ile transkripsiyon (transcription_service.py)
        ↓
6. MarianMT ile çeviri (translation_service.py)
        ↓
7. Cache'e kaydedilir (cache_service.py)
        ↓
8. Response döner
```

## Servis Sorumlulukları

| Servis | Sorumluluk |
|--------|------------|
| CacheService | Video bazlı cache, concurrent request yönetimi |
| YouTubeService | yt-dlp ile ses indirme |
| TranscriptionService | Whisper model yönetimi, transkripsiyon |
| TranslationService | MarianMT model yönetimi, çeviri |

## Singleton Pattern

Tüm servisler singleton olarak tanımlanır:

```python
# Örnek: translation_service.py
translation_service = TranslationService()
```

Bu sayede:
- Model bir kez yüklenir
- Memory verimli kullanılır
- Import ile erişilir

## Lazy Loading

Ağır modeller (Whisper, MarianMT) ilk kullanımda yüklenir:

```python
def _load_model(self):
    if self._model is None:
        self._model = whisper.load_model(...)
    return self._model
```

