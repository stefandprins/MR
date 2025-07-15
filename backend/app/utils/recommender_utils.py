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

def get_aggregated_recommendations(embeddings, input_indices, track_embeddings, valid_track_ids, top_n=5):
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