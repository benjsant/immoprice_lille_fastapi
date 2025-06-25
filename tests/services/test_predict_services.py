import pytest
from app.services.predict_service import PredictService

predict_service = PredictService()

sample_features = {
    "surface_bati": 100,
    "nombre_pieces": 4,
    "type_local": "Appartement",
    "surface_terrain": 0,
    "nombre_lots": 1
}

def test_predict_lille_model():
    result = predict_service.predict("lille", sample_features)
    assert isinstance(result, dict)
    assert "prix_m2_estime" in result
    assert result["ville_modele"] == "Lille"

def test_predict_bordeaux_model():
    result = predict_service.predict("bordeaux", sample_features)
    assert isinstance(result, dict)
    assert "prix_m2_estime" in result
    assert result["ville_modele"] == "Bordeaux"

def test_predict_invalid_city():
    with pytest.raises(ValueError) as exc:
        predict_service.predict("paris", sample_features)
    assert "Ville inconnue" in str(exc.value)
