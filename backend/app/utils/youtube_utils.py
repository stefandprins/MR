import requests
from app.core.config import settings

def get_youtube_url(title, artist):
    query = f"{title} {artist}"
    url = (
        "https://www.googleapis.com/youtube/v3/search"
        f"?part=snippet&type=video&maxResults=1&q={query}&key={settings.YOUTUBE_API_KEY}"
    )
    r = requests.get(url)
    data = r.json()
    if "items" in data and data["items"]:
        video_id = data["items"][0]["id"]["videoId"]
        return f"https://www.youtube.com/watch?v={video_id}"
    return None