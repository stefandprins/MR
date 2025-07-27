from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.api.endpoints import recommender, song  # import other routers here
from app.api.endpoints import search, recommender, youtube_url
from app.core.config import settings

def create_app() -> FastAPI:
    app = FastAPI()

    # Enable CORS for the frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=
        settings.ALLOWED_ORIGINS,  # Vue frontend
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    print("ALLOWED_ORIGINS split:", settings.ALLOWED_ORIGINS)

    # Register API routes
    app.include_router(search.router, tags=["Search"])
    app.include_router(recommender.router, tags=["Recommender"])
    app.include_router(youtube_url.router, tags=["Youtube"])
    # app.include_router(song.router, prefix="/api", tags=["Songs"])  # if you have song API

    return app