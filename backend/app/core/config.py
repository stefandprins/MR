import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env")

# Load environment variables from .env file
# load_dotenv()

class Settings:
    PROJECT_NAME: str = "MR Recommender"
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    # FastAPI settings
    API_PREFIX: str = "/api"

    # CORS
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # Youtube
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

settings = Settings()