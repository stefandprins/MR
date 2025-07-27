from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.youtube_utils import get_youtube_url

class YoutubeInput(BaseModel):
    title: str
    artist_name: str

router = APIRouter()

@router.post("/youtube")
def youtube_url(req: YoutubeInput):
    print(f"Searching for: {req.title} by {req.artist_name}")
    youtube_url = get_youtube_url(req.title, req.artist_name)
    print(f"Result: {youtube_url}")
    if not youtube_url:
        raise HTTPException(status_code=404, detail="YouTube URL not found")

    return {"url": youtube_url}