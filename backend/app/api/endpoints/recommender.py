import os
from fastapi import APIRouter, Query
from sqlalchemy import text
from app.db.database import engine 
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import numpy as np
from app.utils.recommender_utils import get_track_embeddings, get_aggregated_recommendations, get_track_data, preference_filter


class RecommendInput(BaseModel):
    track_ids: List[int]
    genre: Optional[List[str]] = None
    min_year: Optional[int] = None
    max_year: Optional[int] = None
    min_tempo: Optional[float] = None
    max_tempo: Optional[float] = None
    min_duration: Optional[float] = None
    max_duration: Optional[float] = None
    key: Optional[List[int]] = None
    mode: Optional[int] = None
    time_signature: Optional[List[int]] = None

class RecommendResponse(BaseModel):
    id: int
    title: str
    year: Optional[int]
    artist_name: str
    genre: str
    duration: float
    key: int
    mode: int
    tempo: float
    time_signature: int
    youtube_url: Optional[str] = None

router = APIRouter()



@router.post("/recommend", response_model=List[RecommendResponse])
async def retrieve_recommendations(req: RecommendInput):

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    notebook_path = os.path.join(project_root, "notebook")
    
    track_embeddings = np.load(os.path.join(notebook_path, "track_embeddings.npy"))
    valid_track_ids = np.load(os.path.join(notebook_path, "valid_track_ids.npy"))

    # 1) 
    selected_embeddings, input_indices = get_track_embeddings(req.track_ids, track_embeddings, valid_track_ids)

    if selected_embeddings.size == 0 or len(input_indices) == 0:
        print("No embeddings found - returning empty list")
        return []

    recommendations = get_aggregated_recommendations(selected_embeddings, input_indices, track_embeddings, valid_track_ids, top_n=100)

    rows = get_track_data(recommendations, engine)
    
    track_list = rows["recommendations"]

    filtered = [t for t in track_list if preference_filter(t, req)]

    filtered = filtered[:10]

    # for t in filtered:
    #     t["youtube_url"] = get_youtube_url(t["title"], t["artist_name"])

    return filtered
