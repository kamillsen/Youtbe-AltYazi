# 🎬 YouTube Smart Subtitles

YouTube videolarından otomatik altyazı çıkarma ve Türkçe'ye çeviri yapan uygulama.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Özellikler

- 🎵 **YouTube Ses İndirme** - yt-dlp ile yüksek kaliteli ses çıkarma
- 🎙️ **Otomatik Transkripsiyon** - OpenAI Whisper ile konuşmayı metne çevirme
- 🌍 **Türkçe Çeviri** - MarianMT (Helsinki-NLP) ile İngilizce → Türkçe çeviri
- ⚡ **Akıllı Cache** - Video bazlı önbellekleme ile hızlı yanıt
- 🔌 **Chrome Extension** - YouTube'da doğrudan kullanım

## 📁 Proje Yapısı

```
VideoTranslate/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI uygulaması
│   │   ├── config.py               # Yapılandırma ayarları
│   │   ├── models/                 # Pydantic şemaları
│   │   ├── services/               # İş mantığı servisleri
│   │   │   ├── youtube_service.py      # YouTube ses indirme
│   │   │   ├── transcription_service.py # Whisper transkripsiyon
│   │   │   ├── translation_service.py   # MarianMT çeviri
│   │   │   └── cache_service.py         # Cache yönetimi
│   │   ├── routers/                # API endpoint'leri
│   │   └── utils/                  # Yardımcı fonksiyonlar
│   ├── requirements.txt
│   └── run.py
│
└── youtube-extension/              # Chrome eklentisi
    ├── manifest.json
    ├── background.js
    └── content.js
```

## 🚀 Kurulum

### Gereksinimler

- Python 3.10+
- FFmpeg (ses işleme için)

### Adımlar

```bash
# 1. Repoyu klonla
git clone https://github.com/kamillsen/Youtbe-AltYazi.git
cd Youtbe-AltYazi/VideoTranslate/backend

# 2. Sanal ortam oluştur ve aktif et
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 3. Bağımlılıkları kur
pip install -r requirements.txt

# 4. Uygulamayı başlat
python run.py
```

## 📡 API Kullanımı

### Endpoint

```
POST /send_url
```

### Request

```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

### Response

```json
{
  "video_id": "VIDEO_ID",
  "segments": [
    {
      "start": 0.0,
      "end": 3.5,
      "text": "Hello everyone",
      "translated": "Herkese merhaba"
    }
  ]
}
```

### Swagger Docs

API başlatıldıktan sonra: http://127.0.0.1:8000/docs

## 🔧 Yapılandırma

`app/config.py` dosyasından ayarları değiştirebilirsin:

| Ayar | Varsayılan | Açıklama |
|------|------------|----------|
| `WHISPER_MODEL_SIZE` | `base` | Whisper model boyutu (tiny/base/small/medium/large) |
| `TRANSLATION_MODEL_NAME` | `Helsinki-NLP/opus-tatoeba-en-tr` | Çeviri modeli |
| `CACHE_MAX_SIZE` | `4` | Maksimum cache'de tutulacak video sayısı |

## 🧩 Chrome Extension Kurulumu

1. Chrome'da `chrome://extensions` adresine git
2. "Geliştirici modu"nu aç
3. "Paketlenmemiş öğe yükle" tıkla
4. `youtube-extension` klasörünü seç

## 📊 Veri Akışı

```
YouTube URL → Ses İndirme → Whisper Transkripsiyon → MarianMT Çeviri → JSON Response
                                    ↓
                              Cache'e Kaydet
```

## 🛠️ Teknolojiler

- **Backend:** FastAPI, Uvicorn
- **Transkripsiyon:** OpenAI Whisper
- **Çeviri:** Hugging Face Transformers (MarianMT)
- **Ses İndirme:** yt-dlp
- **Extension:** Chrome Manifest V3

## 📄 Lisans

MIT License

---

⭐ Beğendiysen yıldız atmayı unutma!

