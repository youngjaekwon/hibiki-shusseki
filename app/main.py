from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
