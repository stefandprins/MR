import pytest
from fastapi.testclient import TestClient
from app.main import app

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

client = TestClient(app)

def test_search_valid_query():
    # Use a known track or artist in your test DB
    response = client.get("/search?query=Beatles")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:  # Only check keys if any results
        for item in data:
            assert "id" in item
            assert "title" in item
            assert "artist_name" in item

def test_search_empty_query():
    # Should return 422 because of min_length=1
    response = client.get("/search?query=")
    assert response.status_code == 422

def test_search_no_results():
    # Query that should return nothing
    response = client.get("/search?query=asdlkfjasldkfjalsdkjflasdkjflskdjf")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0

def test_search_special_characters():
    # Should not error/crash, and should be safe from SQLi
    special_queries = ["O'Neil", '" OR 1=1 --', "test; DROP TABLE track;"]
    for query in special_queries:
        response = client.get(f"/search?query={query}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


def test_recommend_valid_input():
    # Use valid track_ids present in your test database!
    payload = {"track_ids": [1, 2, 3]}
    response = client.post("/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5      # top_n=5 in your code
    for rec in data:
        # Adjust fields if schema changes
        assert "id" in rec
        assert "title" in rec
        assert "artist_name" in rec
        assert "genre" in rec
        assert "duration" in rec

def test_recommend_invalid_track_ids():
    # Use impossible track ids
    payload = {"track_ids": [9999999, 8888888]}
    response = client.post("/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Could be [] or fewer results; test your actual code logic here
    assert len(data) == 0 or all("id" in rec for rec in data)

def test_recommend_invalid_input():
    # Missing required fields (track_ids)
    payload = {}
    response = client.post("/recommend", json=payload)
    assert response.status_code == 422

# def test_recommend_genre_filter():
#     payload = {"track_ids": [1, 2, 3], "genre": "Rock"}
#     response = client.post("/recommend", json=payload)
#     assert response.status_code == 200
#     data = response.json()
#     assert isinstance(data, list)
#     # If you want to check genre filtering works:
#     if data:  # Only check if any results were returned
#         for rec in data:
#             assert rec["genre"].lower() == "rock"