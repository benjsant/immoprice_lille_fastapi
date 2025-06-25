import joblib
import os 
import pandas as pd 
from typing import Dict 

MODELS_PATH = os.path.join(os.path.dirname(__file__), "..", "models")

class PredictionService: 
    def __init__(self):
        self.models= {
            "lille_appartement": joblib.load(os.path.join(MODELS_PATH,"appartement_xgboost.pkl")),
            "lille_maison": joblib.load(os.path.join(MODELS_PATH,"maison_decision_tree.pkl")),
        }
        self.model_names={
            "lille_appartement": "XGBRegressor",
            "lille_maison": "DecisionTreeRegressor",
        }

    def predict(self, ville: str, features: Dict) -> Dict:
        # On identifie le type de bin (appartement ou maison) pour choisir le modèle
        type_local = features.get("type_local")
        key = f"{ville}_{type_local.lower()}"

        if key not in self.models: 
            raise ValueError(f"Modèle non disponible pour la ville '{ville}'et le type '{type_local}'")
        
        model = self.models[key]

        # Préparer les données dans l'ordre attendu par le modèle
        # On suppose l’ordre : surface_bati, nombre_pieces, type_local, surface_terrain, nombre_lots
        # Attention au type_local (catégorielle) => ici il faut un encodage identique à l'entraînement (à gérer en pipeline)
        # On suppose que le pipeline chargé gère déjà les encodages nécessaires

        X = [[
            features["surface_bati"],
            features["nombre_pieces"],
            features["type_local"],
            features.get("surface_terrain", 0),
            features.get("nombre_lots", 1)
        ]]

        prix_m2_pred = model.predict(X)[0]

        return{
            "prix_m2_estime": round(prix_m2_pred, 2),
            "ville_modele": ville.capitalize(),
            "model": self.model_names[key]
        }
