from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import recommender, song  # import other routers here

def create_app() -> FastAPI:
    app = FastAPI()

    # Enable CORS for the frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],  # Vue frontend
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API routes
    app.include_router(recommender.router, prefix="/api", tags=["Recommender"])
    app.include_router(song.router, prefix="/api", tags=["Songs"])  # if you have song API

    return app