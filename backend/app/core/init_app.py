from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.api.endpoints import recommender, song  # import other routers here
from app.api.endpoints import search, recommender

def create_app() -> FastAPI:
    app = FastAPI()

    origins = [
    "http://localhost:5173",  # for local development
    "https://example.netlify.app",  # placeholder for Netlify
    ]

    # Enable CORS for the frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Vue frontend
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API routes
    app.include_router(search.router, tags=["Search"])
    app.include_router(recommender.router, tags=["Recommender"])
    # app.include_router(song.router, prefix="/api", tags=["Songs"])  # if you have song API

    return app