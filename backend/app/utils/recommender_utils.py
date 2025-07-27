import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from sklearn.metrics.pairwise import cosine_similarity
from app.db.database import engine


def get_track_embeddings(track_ids, track_embeddings, valid_track_ids):
    """
    Get the embeddings for the specified track IDs.
    
    Parameters:
    - track_ids: List of track IDs to retrieve embeddings for.
    - track_embeddings: Numpy array of track embeddings.
    - valid_track_ids: Numpy array of valid track IDs corresponding to the embeddings.
    
    Returns:
    - A dictionary mapping track IDs to their embeddings.
    """
    valid_track_ids = np.array(valid_track_ids)
    selected_embeddings = []
    input_indices = []
    
    for track_id in track_ids:
        track_index = np.where(valid_track_ids == track_id)[0]


        selected_embeddings.append(track_embeddings[track_index].reshape(-1))
        input_indices.append(track_index)
    
    return np.array(selected_embeddings), input_indices

def get_aggregated_recommendations(embeddings, input_indices, track_embeddings, valid_track_ids, top_n=100):
    """
    Get aggregated recommendations based on cosine similarity of track embeddings.
    
    Parameters:
    - embeddings: Numpy array of selected track embeddings.
    - input_indices: List of indices corresponding to the selected embeddings.
    - track_embeddings: Numpy array of all track embeddings.
    - valid_track_ids: Numpy array of valid track IDs corresponding to the embeddings.
    - top_n: Number of top recommendations to return.
    
    Returns:
    - A list of recommended track IDs based on cosine similarity.
    """
    # Compute cosine similarity for each embedding
    similarity_matrix = cosine_similarity(embeddings, track_embeddings)

    # Aggregate across selected tracks (e.g., average similarities)
    aggregated_similarity = np.mean(similarity_matrix, axis=0)

    # Sort descending, exclude selected tracks
    top_indices = aggregated_similarity.argsort()[::-1]
    top_indices = [i for i in top_indices if i not in input_indices][:top_n]

    results = [
        (int(valid_track_ids[i]), float(aggregated_similarity[i]))
        for i in top_indices
    ]

    return results

def get_track_data(recommendations, engine):
    """
    Get track data for the recommended tracks.
    
    Parameters:
    - recommendations: List of tuples (track_id, score) for recommended tracks.
    - engine: SQLAlchemy engine to connect to the database.
    
    Returns:
    - DataFrame containing track details for the recommended tracks.
    """
    # Extract only the track IDs from the recommendations
    similar_track_ids = [track_id for track_id, _ in recommendations]

    # SQL Query
    query = text("""
        SELECT track.*, artist.artist_name, genre.genre
        FROM track
        JOIN artist ON artist.id = track.artist_id
        JOIN genre ON genre.id = track.genre_id
        WHERE track.id = ANY(:track_ids)
    """)

    # Execute query
    with engine.connect() as connection:
        result = connection.execute(query, {"track_ids": similar_track_ids})
        rows = [dict(row._mapping) for row in result]
    # Now rows contain Python-native types: float, str, None, etc.
    return {"recommendations": rows}

def preference_filter(track, pref):
    """
    Apply preference filters to a track.
    
    Parameters:
    - track: Dictionary containing track attributes.
    - pref: Dictionary containing user preferences.
    
    Returns:
    - Boolean indicating if the track matches the preferences.
    """
    track_id = track.get("id", "unknown")
    
    if pref.genre and (track["genre"] is None or track["genre"] not in pref.genre):
        return False
    
    if pref.min_year and (track["year"] is None or track["year"] < pref.min_year):
        return False
    
    if pref.max_year and (track["year"] is None or track["year"] > pref.max_year):
        return False
    
    if pref.min_tempo and (track["tempo"] is None or track["tempo"] < pref.min_tempo):
        return False
    
    if pref.max_tempo and (track["tempo"] is None or track["tempo"] > pref.max_tempo):
        return False
    
    if pref.min_duration and (track["duration"] is None or track["duration"] < pref.min_duration):
        return False
    
    if pref.max_duration and (track["duration"] is None or track["duration"] > pref.max_duration):
        return False
    
    if pref.key and (track["key"] is None or track["key"] not in pref.key):
        return False
    
    if pref.mode is not None and (track["mode"] is None or track["mode"] != pref.mode):
        return False
    
    if pref.time_signature and (track["time_signature"] is None or track["time_signature"] not in pref.time_signature):
        return False
    
    return True