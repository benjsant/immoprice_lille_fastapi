import pytest
from app.services.predict_service import PredictionService
from app.schemas.prediction_schema import PredictResponse

@pytest.mark.asyncio
async def test_predict_success_appartement():
    service = PredictionService()

    payload = {
        "Surface reelle bati": 100,
        "Surface terrain": 0,
        "Nombre de lots": 1,
        "Type local": "Appartement"
    }

    result = await service.predict("lille", payload)

    assert isinstance(result, PredictResponse)
    assert result.ville_modele == "Lille"
    assert result.model is not None
    assert isinstance(result.prix_m2_estime, float)

@pytest.mark.asyncio
async def test_predict_success_maison():
    service = PredictionService()

    payload = {
        "Surface reelle bati": 150,
        "Surface terrain": 300,
        "Nombre de lots": 1,
        "Type local": "Maison"
    }

    result = await service.predict("lille", payload)

    assert isinstance(result, PredictResponse)
    assert result.ville_modele == "Lille"
    assert result.model is not None
    assert isinstance(result.prix_m2_estime, float)

@pytest.mark.asyncio
async def test_predict_raises_unknown_city():
    service = PredictionService()
    payload = {
        "Surface reelle bati": 90,
        "Surface terrain": 10,
        "Nombre de lots": 1,
        "Type local": "Appartement"
    }

    with pytest.raises(ValueError, match="Modèle pour la ville 'paris' non disponible"):
        await service.predict("paris", payload)

@pytest.mark.asyncio
async def test_predict_raises_missing_field():
    service = PredictionService()
    payload = {
        "Surface reelle bati": 90,
        "Surface terrain": 10,
        "Nombre de lots": 1
        # "Type local" manquant
    }

    with pytest.raises(ValueError, match="Le champ 'Type local' est obligatoire"):
        await service.predict("lille", payload)

@pytest.mark.asyncio
async def test_predict_raises_unknown_type_local():
    service = PredictionService()
    payload = {
        "Surface reelle bati": 90,
        "Surface terrain": 10,
        "Nombre de lots": 1,
        "Type local": "Château"
    }

    with pytest.raises(ValueError, match="Modèle pour le type 'Château' à 'lille' non disponible"):
        await service.predict("lille", payload)
