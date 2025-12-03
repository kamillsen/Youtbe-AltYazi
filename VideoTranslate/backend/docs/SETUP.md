# Kurulum Rehberi

## Gereksinimler

- Python 3.10+
- FFmpeg (ses dönüştürme için)
- ~2GB disk alanı (modeller için)

## Adım 1: FFmpeg Kurulumu

```bash
# Fedora
sudo dnf install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

## Adım 2: Python Bağımlılıkları

### uv ile (Önerilen)
```bash
cd backend
uv venv --python 3.10
source .venv/bin/activate
uv pip install -r requirements.txt
```

### pip ile
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Adım 3: NLTK Verileri

İlk çalıştırmada otomatik indirilir. Manuel indirmek için:

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
```

## Adım 4: Çalıştır

```bash
python run.py
```

veya

```bash
uvicorn app.main:app --reload
```

## Sorun Giderme

### SentencePiece hatası
```bash
uv pip install sentencepiece
```

### punkt_tab hatası
```bash
python -c "import nltk; nltk.download('punkt_tab')"
```

### FFmpeg bulunamadı
FFmpeg'in PATH'te olduğundan emin olun:
```bash
which ffmpeg
```

