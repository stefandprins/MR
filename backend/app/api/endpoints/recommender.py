import os
from fastapi import APIRouter
from app.db.database import engine 
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import numpy as np
from app.utils.recommender_utils import get_track_embeddings, get_aggregated_recommendations, get_track_data, preference_filter
from app.utils.recommender_utils import get_matched_preferences, calc_preference_coverage, calc_distribution, calc_average_similarity
from app.utils.recommender_utils import tempo_distribution, keys_to_str

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
    similarity: float
    matched_preferences: list[str] = []

class AnalyticsResponse(BaseModel):
    preference_coverage: Dict[str, int]
    genre_distribution: Dict[str, int]
    key_distribution: Optional[Dict[str, int]] = None
    mode_distribution: Optional[Dict[str, int]] = None
    time_signature_distribution: Optional[Dict[str, int]] = None
    average_similarity: Optional[float]
    tempo_distribution: Optional[Dict[str, int]] = None

class RecommendResultsResponse(BaseModel):
    recommendations: List[RecommendResponse]
    analytics: AnalyticsResponse

router = APIRouter()

@router.post("/recommend", response_model=RecommendResultsResponse)
async def retrieve_recommendations(req: RecommendInput):

    # Get the correct path to the notebook directory.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    notebook_path = os.path.join(project_root, "notebook")
    
    # Load precomputed embeddings and valid track IDs.
    track_embeddings = np.load(os.path.join(notebook_path, "track_embeddings.npy"))
    valid_track_ids = np.load(os.path.join(notebook_path, "valid_track_ids.npy"))

    # Fetch embeddings for input track IDs.
    selected_embeddings, input_indices = get_track_embeddings(req.track_ids, track_embeddings, valid_track_ids)

    # Handle case where no embeddings are found.
    if selected_embeddings.size == 0 or len(input_indices) == 0:
        print("No embeddings found - returning empty list")
        return {
            "recommendations": [],
            "analytics": {
                "preference_coverage": {},
                "genre_distribution": {},
                "key_distribution": {},
                "mode_distribution": {},
                "time_signature_distribution": {},
                "average_similarity": 0.0,
                "tempo_distribution": {}
            }
        }

    # Get aggregated recommendations.
    recommendations = get_aggregated_recommendations(selected_embeddings, input_indices, track_embeddings, valid_track_ids, top_n=100)
    
    similarity_map = {track_id: sim for track_id, sim in recommendations}

    rows = get_track_data(recommendations, engine)
    track_list = rows["recommendations"]

    for t in track_list:
        t["similarity"] = similarity_map.get(t["id"], None)
        t["matched_preferences"] = get_matched_preferences(t, req)

    filtered = [t for t in track_list if preference_filter(t, req)]
    filtered.sort(key=lambda x: x.get("similarity", 0), reverse=True)
    filtered = filtered[:10]

    genre_distribution = calc_distribution(filtered, "genre")
    key_distribution = calc_distribution(filtered, "key")
    mode_distribution = calc_distribution(filtered, "mode")
    time_signature_distribution = calc_distribution(filtered, "time_signature")

    analytics = {
    "preference_coverage": calc_preference_coverage(filtered, req),
    "genre_distribution": genre_distribution,
    "key_distribution": keys_to_str(key_distribution),
    "mode_distribution": keys_to_str(mode_distribution),
    "time_signature_distribution": keys_to_str(time_signature_distribution),
    "average_similarity": calc_average_similarity(filtered),
    "tempo_distribution": tempo_distribution(filtered)
}

    return {
    "recommendations": filtered,
    "analytics": analytics
}
