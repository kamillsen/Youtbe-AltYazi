"""
FastAPI uygulama başlatma ve yapılandırma
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import (
    CORS_ORIGINS,
    CORS_ALLOW_CREDENTIALS,
    CORS_ALLOW_METHODS,
    CORS_ALLOW_HEADERS
)
from .routers import subtitle_router


def create_app() -> FastAPI:
    """
    FastAPI uygulamasını oluştur ve yapılandır.
    
    Returns:
        Yapılandırılmış FastAPI instance
    """
    app = FastAPI(
        title="YouTube Smart Subtitles API",
        description="YouTube videolarından altyazı çıkarma ve çeviri servisi",
        version="2.0.0"
    )
    
    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=CORS_ALLOW_CREDENTIALS,
        allow_methods=CORS_ALLOW_METHODS,
        allow_headers=CORS_ALLOW_HEADERS,
    )
    
    # Router'ları ekle
    app.include_router(subtitle_router.router)
    
    return app


# Uygulama instance'ı
app = create_app()


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "YouTube Smart Subtitles API",
        "version": "2.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Sağlık kontrolü endpoint"""
    return {"status": "healthy"}

