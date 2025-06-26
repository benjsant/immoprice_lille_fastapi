import os
import joblib
import pandas as pd
from app.schemas.prediction_schema import PredictResponse
from app.model_loader import load_model

class PredictionService:
    def __init__(self):
        self.models = {
            "lille": {
                "Appartement": load_model("appartement_xgboost.pkl"),
                "Maison": load_model("maison_decision_tree.pkl"),
            }
        }

        self.expected_columns = [
            "Surface reelle bati",
            "Surface terrain",
            "Nombre de lots",
            "Type local"
        ]

    async def predict(self, ville: str, features: dict) -> PredictResponse:
        ville = ville.lower()

        if ville not in self.models:
            raise ValueError(f"Modèle pour la ville '{ville}' non disponible")

        if "Type local" not in features:
            raise ValueError("Le champ 'Type local' est obligatoire dans les données.")

        logement_type = features["Type local"]

        if logement_type not in self.models[ville]:
            raise ValueError(f"Modèle pour le type '{logement_type}' à '{ville}' non disponible")

        df = pd.DataFrame([features])

        missing_cols = set(self.expected_columns) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Colonnes manquantes dans les données : {missing_cols}")

        model = self.models[ville][logement_type]

        # La prédiction est CPU-bound et synchrone, on la laisse telle quelle
        prediction = model.predict(df)[0]

        try:
            model_name = type(model.named_steps["model"]).__name__
        except Exception:
            model_name = type(model).__name__

        return PredictResponse(
            prix_m2_estime=round(float(prediction), 2),
            ville_modele=ville.capitalize(),
            model=model_name
        )
