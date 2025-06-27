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
    """
    Teste la prédiction réussie pour la ville de Lille.

    Envoie une requête POST avec un payload valide et vérifie que la réponse 
    a un code de statut 200, que le champ 'prix_m2_estime' est présent dans 
    la réponse, que la ville du modèle est 'Lille', et que le nom du modèle 
    n'est pas vide.
    """
    response = client.post("/predict/lille", json=valid_payload)
    assert response.status_code == 200
    data = response.json()
    assert "prix_m2_estime" in data
    assert data["ville_modele"] == "Lille"
    assert data["model"] != ""

def test_predict_lille_missing_field():
    """
    Teste la gestion des champs manquants pour la prédiction à Lille.

    Envoie une requête POST sans le champ 'Type local' et vérifie que la 
    réponse a un code de statut 422 et que le message d'erreur contient 
    'Type local'.
    """
    payload = valid_payload.copy()
    del payload["Type local"]  # Champ manquant
    response = client.post("/predict/lille", json=payload)
    assert response.status_code == 422
    assert "Type local" in response.text

def test_predict_bordeaux_not_implemented():
    """
    Teste la réponse pour la ville de Bordeaux qui n'est pas encore implémentée.

    Envoie une requête POST pour Bordeaux et vérifie que la réponse a un 
    code de statut 501 et que le message d'erreur contient 'pas encore 
    implémenté'.
    """
    response = client.post("/predict/bordeaux", json=valid_payload)
    assert response.status_code == 501
    assert "pas encore implémenté" in response.text

def test_predict_dynamic_success():
    """
    Teste la prédiction réussie avec une requête dynamique.

    Envoie une requête POST avec un payload dynamique contenant la ville 
    et les caractéristiques, et vérifie que la réponse a un code de statut 
    200 et que le champ 'prix_m2_estime' est présent dans la réponse.
    """
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
    """
    Teste la gestion des champs manquants dans une requête dynamique.

    Envoie une requête POST sans le champ 'Type local' dans les 
    caractéristiques et vérifie que la réponse a un code de statut 422 
    et que le message d'erreur contient 'Type local'.
    """
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
    """
    Teste la gestion des villes inconnues dans une requête dynamique.

    Envoie une requête POST avec une ville inconnue (Paris) et vérifie 
    que la réponse a un code de statut 400 et que le message d'erreur 
    contient 'Ville inconnue'.
    """
    payload = {
        "ville": "paris",
        "features": valid_payload
    }
    response = client.post("/predict/", json=payload)
    assert response.status_code == 400
    assert "Ville inconnue" in response.text

def test_predict_dynamic_bordeaux_not_implemented():
    """
    Teste la réponse pour la ville de Bordeaux dans une requête dynamique 
    qui n'est pas encore implémentée.

    Envoie une requête POST pour Bordeaux et vérifie que la réponse a un 
    code de statut 501 et que le message d'erreur contient 'pas encore 
    implémenté'.
    """
    payload = {
        "ville": "bordeaux",
        "features": valid_payload
    }
    response = client.post("/predict/", json=payload)
    assert response.status_code == 501
    assert "pas encore implémenté" in response.text
