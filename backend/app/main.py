"""
Urukais Klick - API Principal
FastAPI backend para la aplicación de descubrimiento musical
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import users, tracks, auth, upload, moods, recommendations, social, streaming, live, youtube

app = FastAPI(
    title="Urukais Klick API",
    description="API gratuita para descubrimiento musical y conexión artística",
    version="1.0.0"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router, prefix=settings.API_V1_STR + "/auth", tags=["auth"])
app.include_router(users.router, prefix=settings.API_V1_STR + "/users", tags=["users"])
app.include_router(tracks.router, prefix=settings.API_V1_STR + "/tracks", tags=["tracks"])
app.include_router(upload.router, prefix=settings.API_V1_STR + "/upload", tags=["upload"])
app.include_router(moods.router, prefix=settings.API_V1_STR + "/moods", tags=["moods"])
app.include_router(recommendations.router, prefix=settings.API_V1_STR + "/recommendations", tags=["recommendations"])
app.include_router(social.router, prefix=settings.API_V1_STR + "/social", tags=["social"])
app.include_router(streaming.router, prefix=settings.API_V1_STR + "/streaming", tags=["streaming"])
app.include_router(live.router, prefix=settings.API_V1_STR + "/live", tags=["live"])
app.include_router(youtube.router, prefix=settings.API_V1_STR + "/youtube", tags=["youtube"])

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a Urukais Klick API",
        "version": "1.0.0",
        "status": "operativo"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
