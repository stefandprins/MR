import os
from fastapi import APIRouter, Query
from sqlalchemy import text
from app.db.database import engine 
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import numpy as np
from app.utils.recommender_utils import get_track_embeddings, get_aggregated_recommendations, get_track_data

class RecommendInput(BaseModel):
    track_ids: List[int]
    genre: Optional[str] = None

class RecommendResponse(BaseModel):
    id: int
    title: str
    year: Optional[int]
    artist_name: str
    genre: str
    duration: float

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
        return []

    recommendations = get_aggregated_recommendations(selected_embeddings, input_indices, track_embeddings, valid_track_ids, top_n=5)

    rows = get_track_data(recommendations, engine)

    return rows["recommendations"]