import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from sklearn.metrics.pairwise import cosine_similarity
from app.db.database import engine
from collections import Counter


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

def get_matched_preferences(track, pref):
    """    Get the list of matched preferences for a track.
    Parameters:
    - track: Dictionary containing track attributes.
    - pref: Dictionary containing user preferences.
    Returns:
    - List of matched preference keys.
    """
    matched = []
    if pref.genre and track["genre"] in pref.genre:
        matched.append("genre")
    if pref.min_year and track["year"] and track["year"] >= pref.min_year:
        matched.append("min_year")
    if pref.max_year and track["year"] and track["year"] <= pref.max_year:
        matched.append("max_year")
    if pref.min_tempo and track["tempo"] and track["tempo"] >= pref.min_tempo:
        matched.append("min_tempo")
    if pref.max_tempo and track["tempo"] and track["tempo"] <= pref.max_tempo:
        matched.append("max_tempo")
    if pref.min_duration and track["duration"] and track["duration"] >= pref.min_duration:
        matched.append("min_duration")
    if pref.max_duration and track["duration"] and track["duration"] <= pref.max_duration:
        matched.append("max_duration")
    if pref.key and track["key"] in pref.key:
        matched.append("key")
    if pref.mode is not None and track["mode"] == pref.mode:
        matched.append("mode")
    if pref.time_signature and track["time_signature"] in pref.time_signature:
        matched.append("time_signature")
    return matched

def calc_preference_coverage(recommended_tracks, user_prefs):
    # Count matches per preference
    coverage = {
        "genre": 0,
        "key": 0,
        "mode": 0,
        "time_signature": 0,
        "tempo": 0,
        "duration": 0,
        # ...add any others you use
    }
    for track in recommended_tracks:
        if user_prefs.genre and track["genre"] in user_prefs.genre:
            coverage["genre"] += 1
        if user_prefs.key and track["key"] in user_prefs.key:
            coverage["key"] += 1
        if user_prefs.mode is not None and track["mode"] == user_prefs.mode:
            coverage["mode"] += 1
        if user_prefs.time_signature and track["time_signature"] in user_prefs.time_signature:
            coverage["time_signature"] += 1
        if user_prefs.min_tempo and track["tempo"] >= user_prefs.min_tempo:
            coverage["tempo"] += 1
        if user_prefs.max_tempo and track["tempo"] <= user_prefs.max_tempo:
            coverage["tempo"] += 1
        if user_prefs.min_duration and track["duration"] >= user_prefs.min_duration:
            coverage["duration"] += 1
        if user_prefs.max_duration and track["duration"] <= user_prefs.max_duration:
            coverage["duration"] += 1
    return coverage

def calc_average_similarity(recommended_tracks):
    sims = [track.get("similarity") for track in recommended_tracks if "similarity" in track]
    return float(np.mean(sims)) if sims else None

def calc_distribution(tracks, field):
    return dict(Counter(track[field] for track in tracks if track[field] is not None))

def bin_tempo(tempo):
    if tempo < 80:
        return "60–80"
    elif tempo < 100:
        return "80–100"
    elif tempo < 120:
        return "100–120"
    elif tempo < 140:
        return "120–140"
    elif tempo < 160:
        return "140–160"
    else:
        return "160+"

def tempo_distribution(tracks):
    bins = [bin_tempo(track["tempo"]) for track in tracks if track.get("tempo") is not None]
    from collections import Counter
    return dict(Counter(bins))

def keys_to_str(d):
    """Convert all keys in a dict to strings."""
    return {str(k): v for k, v in d.items()}