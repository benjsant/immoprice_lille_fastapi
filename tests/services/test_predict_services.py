import pytest
from app.services.predict_service import PredictionService
from app.schemas.prediction_schema import PredictResponse

@pytest.mark.asyncio
async def test_predict_success_appartement():
    """
    Teste la prédiction réussie pour un appartement.

    Crée un service de prédiction et envoie un payload valide pour un appartement 
    à Lille. Vérifie que le résultat est une instance de PredictResponse, que 
    la ville du modèle est 'Lille', que le modèle n'est pas None, et que le 
    prix estimé par mètre carré est un float.
    """
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
    """
    Teste la prédiction réussie pour une maison.

    Crée un service de prédiction et envoie un payload valide pour une maison 
    à Lille. Vérifie que le résultat est une instance de PredictResponse, que 
    la ville du modèle est 'Lille', que le modèle n'est pas None, et que le 
    prix estimé par mètre carré est un float.
    """
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
    """
    Teste la gestion des villes inconnues.

    Crée un service de prédiction et envoie un payload valide pour un appartement 
    à Paris. Vérifie que la méthode lève une exception ValueError avec le message 
    approprié indiquant que le modèle pour la ville 'paris' n'est pas disponible.
    """
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
    """
    Teste la gestion des champs manquants.

    Crée un service de prédiction et envoie un payload sans le champ 'Type local' 
    pour un appartement à Lille. Vérifie que la méthode lève une exception 
    ValueError avec le message approprié indiquant que le champ 'Type local' est 
    obligatoire.
    """
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
    """
    Teste la gestion des types de local inconnus.

    Crée un service de prédiction et envoie un payload avec un type de local 
    inconnu ('Château') pour un appartement à Lille. Vérifie que la méthode lève 
    une exception ValueError avec le message approprié indiquant que le modèle 
    pour le type 'Château' à 'lille' n'est pas disponible.
    """
    service = PredictionService()
    payload = {
        "Surface reelle bati": 90,
        "Surface terrain": 10,
        "Nombre de lots": 1,
        "Type local": "Château"
    }

    with pytest.raises(ValueError, match="Modèle pour le type 'Château' à 'lille' non disponible"):
        await service.predict("lille", payload)
