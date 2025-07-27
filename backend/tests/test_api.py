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
    assert len(data) <= 10      # top_n=5 in your code
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
    assert len(data) == 0

def test_recommend_invalid_input():
    # Missing required fields (track_ids)
    payload = {}
    response = client.post("/recommend", json=payload)
    assert response.status_code == 422

def test_recommend_genre_filter():
    payload = {"track_ids": [1, 2, 3], "genre": ["Rock", "Pop"]}
    response = client.post("/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        for rec in data:
            assert rec["genre"] in ["Rock", "Pop"]

def test_recommend_year_tempo_duration_filter():
    payload = {
        "track_ids": [1, 2, 3],
        "min_year": 1990, "max_year": 2000,
        "min_tempo": 100, "max_tempo": 150,
        "min_duration": 180, "max_duration": 240
    }
    response = client.post("/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for rec in data:
        assert 1990 <= rec["year"] <= 2000
        assert 100 <= rec["tempo"] <= 150
        assert 180 <= rec["duration"] <= 240

def test_recommend_key_mode_filter():
    payload = {"track_ids": [1, 2, 3], "key": [0, 2, 5], "mode": 1}
    response = client.post("/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    print(data)
    for rec in data:
        assert rec["key"] in [0, 2, 5]
        assert rec["mode"] == 1

def test_recommend_time_signature_filter():
    payload = {"track_ids": [1, 2, 3], "time_signature": [4]}
    response = client.post("/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    for rec in data:
        assert rec["time_signature"] == 4


def test_youtube_url_success():
    payload = {
        "title": "School",
        "artist_name": "Nirvana"
    }
    response = client.post("/youtube", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "url" in data
    if data["url"] is None:
        print("No URL returned, possibly due to quota exhaustion. Full response:", data)
        # Optionally: return here to not check further asserts
        return
    # Only check the content if there was a URL returned!
    assert "School" in data["url"]
    assert "Nirvana" in data["url"]

def test_youtube_url_missing_title():
    payload = {"artist_name": "Nirvana"}
    response = client.post("/youtube", json=payload)
    assert response.status_code == 422  # Unprocessable Entity

def test_youtube_url_missing_artist():
    payload = {"title": "School"}
    response = client.post("/youtube", json=payload)
    assert response.status_code == 422  # Unprocessable Entity

def test_youtube_url_empty_strings():
    payload = {"title": "", "artist_name": ""}
    response = client.post("/youtube", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "url" in data