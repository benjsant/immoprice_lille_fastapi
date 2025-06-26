import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

valid_payload = {
    "Surface reelle bati": 100,
    "Surface terrain": 0,
    "Nombre de lots": 1,
    "Type local": "Appartement"
}

def test_predict_lille_success():
    response = client.post("/predict/lille", json=valid_payload)
    assert response.status_code == 200
    data = response.json()
    assert "prix_m2_estime" in data
    assert data["ville_modele"] == "Lille"
    assert data["model"] != ""

def test_predict_lille_missing_field():
    payload = valid_payload.copy()
    del payload["Type local"]  # Champ manquant
    response = client.post("/predict/lille", json=payload)
    assert response.status_code == 422
    assert "Type local" in response.text

def test_predict_bordeaux_not_implemented():
    response = client.post("/predict/bordeaux", json=valid_payload)
    assert response.status_code == 501
    assert "pas encore implémenté" in response.text

def test_predict_dynamic_success():
    payload = {
        "ville": "lille",
        "features": valid_payload
    }
    response = client.post("/predict/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "prix_m2_estime" in data
    assert data["ville_modele"] == "Lille"

def test_predict_dynamic_missing_fields():
    payload = {
        "ville": "lille",
        "features": {
            "Surface reelle bati": 100,
            "Surface terrain": 0,
            "Nombre de lots": 1,
            # "Type local" manquant ici
        }
    }
    response = client.post("/predict/", json=payload)
    assert response.status_code == 422
    assert "Type local" in response.text

def test_predict_dynamic_unknown_city():
    payload = {
        "ville": "paris",
        "features": valid_payload
    }
    response = client.post("/predict/", json=payload)
    assert response.status_code == 400
    assert "Ville inconnue" in response.text

def test_predict_dynamic_bordeaux_not_implemented():
    payload = {
        "ville": "bordeaux",
        "features": valid_payload
    }
    response = client.post("/predict/", json=payload)
    assert response.status_code == 501
    assert "pas encore implémenté" in response.text
