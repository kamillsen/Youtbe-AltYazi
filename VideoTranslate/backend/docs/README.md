# YouTube Smart Subtitles - Backend

YouTube videolarından otomatik altyazı çıkarma ve Türkçe'ye çeviri API servisi.

## Özellikler

- YouTube videolarından ses indirme (yt-dlp)
- Whisper ile transkripsiyon
- MarianMT ile İngilizce → Türkçe çeviri
- Video bazlı cache sistemi
- RESTful API (FastAPI)

## Hızlı Başlangıç

```bash
# Sanal ortam aktif et
source .venv/bin/activate

# Çalıştır
python run.py
```

API: http://127.0.0.1:8000
Docs: http://127.0.0.1:8000/docs

## Dokümantasyon

- [API Referansı](API.md)
- [Kurulum Rehberi](SETUP.md)
- [Mimari](ARCHITECTURE.md)

