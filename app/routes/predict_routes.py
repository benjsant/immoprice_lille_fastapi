from fastapi import APIRouter, HTTPException
from app.schemas.prediction_schema import PredictRequest, PredictDirectRequest, PredictResponse
from app.services.predict_service import PredictionService

router = APIRouter(prefix="/predict", tags=["Prédiction"])
service = PredictionService()

@router.post("/lille", response_model=PredictResponse)
async def predict_lille(features: PredictDirectRequest):
    """
    Prédit les résultats pour la ville de Lille en utilisant les caractéristiques fournies.

    Parameters:
    ----------
    features : PredictDirectRequest
        Un objet contenant les caractéristiques nécessaires pour effectuer la prédiction.

    Returns:
    -------
    PredictResponse
        Un objet contenant les résultats de la prédiction.

    Raises:
    ------
    HTTPException
        Si une erreur se produit lors de la prédiction, une exception HTTP 400 est levée 
        avec le message d'erreur.
    """
    try:
        result = await service.predict("lille", features.model_dump(by_alias=True))
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/bordeaux", response_model=PredictResponse)
async def predict_bordeaux(features: PredictDirectRequest):
    """
    Endpoint pour prédire les résultats pour la ville de Bordeaux.

    Cette fonction lève une exception HTTP 501 car le modèle pour Bordeaux n'est pas 
    encore implémenté.

    Parameters:
    ----------
    features : PredictDirectRequest
        Un objet contenant les caractéristiques nécessaires pour effectuer la prédiction.

    Returns:
    -------
    HTTPException
        Une exception HTTP 501 indiquant que le modèle pour Bordeaux n'est pas encore 
        implémenté.
    """
    raise HTTPException(status_code=501, detail="Modèle Bordeaux pas encore implémenté")

@router.post("/", response_model=PredictResponse)
async def predict(payload: PredictRequest):
    """
    Prédit les résultats en fonction de la ville et des caractéristiques fournies dans 
    la requête.

    Parameters:
    ----------
    payload : PredictRequest
        Un objet contenant le nom de la ville et les caractéristiques nécessaires pour 
        effectuer la prédiction.

    Returns:
    -------
    PredictResponse
        Un objet contenant les résultats de la prédiction.

    Raises:
    ------
    HTTPException
        Si les champs 'ville' ou 'features' sont manquants, ou si la ville est inconnue, 
        une exception HTTP 400 est levée. Si le modèle pour Bordeaux est demandé, une 
        exception HTTP 501 est levée.
    """
    if not payload.ville or not payload.features:
        raise HTTPException(status_code=400, detail="Les champs 'ville' et 'features' sont requis")

    ville = payload.ville.lower()
    if ville not in ("lille", "bordeaux"):
        raise HTTPException(status_code=400, detail=f"Ville inconnue : {ville}")

    if ville == "bordeaux":
        raise HTTPException(status_code=501, detail="Modèle Bordeaux pas encore implémenté")

    try:
        result = await service.predict(ville, payload.features.model_dump(by_alias=True))
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

