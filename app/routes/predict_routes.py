from fastapi import APIRouter, HTTPException 
from app.schemas.prediction_schema import PredictRequest, PredictDirectRequest, PredictResponse
from app.services.predict_service import PredictionService

router = APIRouter(prefix="/predict", tags=["Prédiction"])

service = PredictionService

@router.post("/lille", response_model=PredictResponse)
def predict_lille(features: PredictDirectRequest): 
    try: 
        result = service.predict("lille", features.dict())
        return result
    except Exception as e: 
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/bordeaux", response_model=PredictResponse)
def predict_bordeaux(features: PredictDirectRequest):
    # Comme on n'a pas de modèle bordeaux, on peut retourner une erreur ou re-router vers Lille
    raise HTTPException(status_code=501, detail="Modèle Bordeaux non encore implémenté")

@router.post("/", response_model=PredictResponse)
def predict(payload: PredictRequest):
    if not payload.ville or not payload.features:
        raise HTTPException(status_code=400, detail="Le champ 'ville' et 'features' sont requis")

    ville = payload.ville.lower()
    if ville not in ("lille", "bordeaux"):
        raise HTTPException(status_code=400, detail=f"Ville inconnue : {ville}")

    if ville == "bordeaux":
        raise HTTPException(status_code=501, detail="Modèle Bordeaux non encore implémenté")

    try:
        result = service.predict(ville, payload.features.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))