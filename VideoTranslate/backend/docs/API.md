# API Referansı

Base URL: `http://127.0.0.1:8000`

---

## Endpoints

### GET /
API bilgisi döndürür.

**Response:**
```json
{
  "message": "YouTube Smart Subtitles API",
  "version": "2.0.0",
  "docs": "/docs"
}
```

---

### GET /health
Sağlık kontrolü.

**Response:**
```json
{
  "status": "healthy"
}
```

---

### POST /send_url
YouTube video URL'sinden altyazı üretir.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Response (Başarılı):**
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

**Response (Hata):**
```json
{
  "success": false,
  "error": "Hata mesajı"
}
```

---

## Swagger UI

Interaktif API dokümantasyonu: http://127.0.0.1:8000/docs

