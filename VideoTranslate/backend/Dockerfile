FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/opt/huggingface \
    TRANSFORMERS_CACHE=/opt/huggingface \
    WHISPER_CACHE_DIR=/opt/whisper \
    NLTK_DATA=/opt/nltk_data \
    CUDA_VISIBLE_DEVICES=0

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    ffmpeg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install -r requirements.txt

# Pre-download models and data for offline operation
RUN python3 - <<'PY'
import os
import whisper
import nltk
from transformers import MarianTokenizer, MarianMTModel

os.makedirs('/opt/huggingface', exist_ok=True)
os.makedirs('/opt/whisper', exist_ok=True)
os.makedirs('/opt/nltk_data', exist_ok=True)

# NLTK
nltk.download('punkt', download_dir='/opt/nltk_data')
nltk.download('punkt_tab', download_dir='/opt/nltk_data')

# Whisper
whisper.load_model('base', download_root='/opt/whisper')

# MarianMT
model_name = 'Helsinki-NLP/opus-tatoeba-en-tr'
MarianTokenizer.from_pretrained(model_name, cache_dir='/opt/huggingface')
MarianMTModel.from_pretrained(model_name, cache_dir='/opt/huggingface')

print('Offline assets ready.')
PY

COPY app ./app
COPY run.py ./run.py

ENV TRANSFORMERS_OFFLINE=1 \
    HF_HUB_OFFLINE=1

EXPOSE 8000

CMD ["python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
