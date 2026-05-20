# YouTube Smart Subtitles

YouTube videolarından ses alıp otomatik altyazı çıkaran ve İngilizce metni Türkçe'ye çeviren FastAPI tabanlı servis.

## Özellikler

- YouTube ses indirme (`yt-dlp`)
- Whisper ile transkripsiyon
- MarianMT ile İngilizce → Türkçe çeviri
- Basit cache mekanizması
- Chrome extension ile entegrasyon

## Proje Yapısı

- `/home/runner/work/Youtbe-AltYazi/Youtbe-AltYazi/VideoTranslate/backend` → API servisi
- `/home/runner/work/Youtbe-AltYazi/Youtbe-AltYazi/VideoTranslate/youtube-extension` → Chrome eklentisi

## Lokal (Python) Çalıştırma

```bash
cd /home/runner/work/Youtbe-AltYazi/Youtbe-AltYazi/VideoTranslate/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

API: `http://127.0.0.1:8000`  
Docs: `http://127.0.0.1:8000/docs`

---

## Docker ile Çalıştırma (Offline + GPU 0)

Aşağıdaki Dockerfile build sırasında gerekli model/artifact indirmelerini yapar:

- Whisper `base` modeli
- MarianMT `Helsinki-NLP/opus-tatoeba-en-tr`
- NLTK: `punkt`, `punkt_tab`

Bu sayede image build edildikten sonra container internet olmadan çalışır.

### 1) Build

```bash
cd /home/runner/work/Youtbe-AltYazi/Youtbe-AltYazi/VideoTranslate/backend
docker build -t youtube-smart-subtitles:offline-gpu0 .
```

### 2) Çalıştır (yalnızca GPU 0)

```bash
docker run --rm \
  --gpus '"device=0"' \
  -e CUDA_VISIBLE_DEVICES=0 \
  -p 8000:8000 \
  youtube-smart-subtitles:offline-gpu0
```

Servis container içinde `0.0.0.0:8000` üzerinde açılır.

### 3) Offline makineye taşıma

Online makinede image’ı export et:

```bash
docker save youtube-smart-subtitles:offline-gpu0 -o youtube-smart-subtitles-offline-gpu0.tar
```

Offline makinede import et:

```bash
docker load -i youtube-smart-subtitles-offline-gpu0.tar
```

Sonra yine aynı `docker run` komutuyla başlat.

> Not: Offline makinede NVIDIA driver + nvidia-container-toolkit kurulu olmalıdır.

---

## API

### `POST /send_url`

Request:

```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

Örnek response:

```json
{
  "success": true,
  "cached": false,
  "subtitles": [
    {
      "start": 0.0,
      "end": 2.5,
      "text": "Hello world",
      "translation": "Merhaba dünya"
    }
  ]
}
```

Health: `GET /health`

## Lisans

MIT
