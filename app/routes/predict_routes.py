from fastapi import APIRouter, HTTPException
from app.schemas.prediction_schema import PredictRequest, PredictDirectRequest, PredictResponse
from app.services.predict_service import PredictionService

router = APIRouter(prefix="/predict", tags=["Prédiction"])
service = PredictionService()

@router.post("/lille", response_model=PredictResponse)
async def predict_lille(features: PredictDirectRequest):
    try:
        result = await service.predict("lille", features.model_dump(by_alias=True))
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/bordeaux", response_model=PredictResponse)
async def predict_bordeaux(features: PredictDirectRequest):
    raise HTTPException(status_code=501, detail="Modèle Bordeaux pas encore implémenté")

@router.post("/", response_model=PredictResponse)
async def predict(payload: PredictRequest):
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

