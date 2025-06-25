import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

valid_payload = {
    "surface_bati": 100,
    "nombre_pieces": 4,
    "type_local": "Appartement",
    "surface_terrain": 0,
    "nombre_lots": 1
}

def test_predict_lille_success():
    response = client.post("/predict/lille", json=valid_payload)
    assert response.status_code == 200
    data = response.json()
    assert "prix_m2_estime" in data
    assert data["ville_modele"].lower() == "lille"

def test_predict_bordeaux_success():
    response = client.post("/predict/bordeaux", json=valid_payload)
    assert response.status_code == 200
    data = response.json()
    assert "prix_m2_estime" in data
    assert data["ville_modele"].lower() == "bordeaux"

def test_predict_dynamic_success():
    payload = {
        "ville": "lille",
        "features": valid_payload
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["ville_modele"].lower() == "lille"

def test_predict_dynamic_invalid_city():
    payload = {
        "ville": "paris",
        "features": valid_payload
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 400
    assert "Ville inconnue" in response.json()["detail"]
