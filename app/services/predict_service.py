import os
import joblib
import pandas as pd
from app.schemas.prediction_schema import PredictResponse
from app.model_loader import load_model

class PredictionService:
    """
    Service de prédiction pour estimer le prix au mètre carré en fonction des 
    caractéristiques d'une propriété.

    Attributes:
    ----------
    models : dict
        Dictionnaire contenant les modèles de prédiction chargés pour chaque ville 
        et type de logement.
        
    expected_columns : list
        Liste des colonnes attendues dans les données d'entrée pour effectuer une 
        prédiction.
    """
    def __init__(self):
        """
        Initialise le service de prédiction en chargeant les modèles pour les villes 
        et types de logements disponibles.
        """
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
        """
        Effectue une prédiction du prix au mètre carré en fonction de la ville et des 
        caractéristiques fournies.

        Parameters:
        ----------
        ville : str
            Le nom de la ville pour laquelle la prédiction est demandée.
        
        features : dict
            Un dictionnaire contenant les caractéristiques de la propriété, y compris 
            la surface, le nombre de lots et le type de local.

        Returns:
        -------
        PredictResponse
            Un objet contenant le prix estimé par mètre carré, la ville du modèle 
            utilisé et le nom du modèle.

        Raises:
        ------
        ValueErrors
            Si la ville n'est pas disponible, si le type de local est manquant ou 
            non valide, ou si des colonnes attendues sont manquantes dans les données.
        """
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
