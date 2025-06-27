from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

class PredictDirectRequest(BaseModel):
    """
    Modèle de données pour les requêtes de prédiction directe.

    Attributes:
    ----------
    surface_reelle_bati : float
        La surface réelle bâtie de la propriété, en mètres carrés.
        
    surface_terrain : float
        La surface du terrain de la propriété, en mètres carrés.
        
    nombre_de_lots : float
        Le nombre de lots associés à la propriété.
        
    type_local : Literal["Appartement", "Maison"]
        Le type de local, qui peut être soit "Appartement" soit "Maison".

    Config:
    -------
    model_config : ConfigDict
        Configuration du modèle Pydantic pour peupler les attributs par nom et interdire 
        les attributs supplémentaires non définis.
    """
    surface_reelle_bati: float = Field(..., alias="Surface reelle bati")
    surface_terrain: float = Field(..., alias="Surface terrain")
    nombre_de_lots: float = Field(..., alias="Nombre de lots")
    type_local: Literal["Appartement", "Maison"] = Field(..., alias="Type local")

    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid"
    )


class PredictRequest(BaseModel):
    """
    Modèle de données pour les requêtes de prédiction.

    Attributes:
    ----------
    ville : str
        Le nom de la ville pour laquelle la prédiction est demandée.
        
    features : PredictDirectRequest
        Un objet contenant les caractéristiques nécessaires pour effectuer la prédiction.
    """"""
    Modèle de données pour les requêtes de prédiction.

    Attributes:
    ----------
    ville : str
        Le nom de la ville pour laquelle la prédiction est demandée.
        
    features : PredictDirectRequest
        Un objet contenant les caractéristiques nécessaires pour effectuer la prédiction.
    """
    ville: str
    features: PredictDirectRequest


class PredictResponse(BaseModel):
    """
    Modèle de données pour les réponses de prédiction.

    Attributes:
    ----------
    prix_m2_estime : float
        Le prix estimé par mètre carré pour la propriété.
        
    ville_modele : str
        Le nom de la ville pour laquelle le modèle a été entraîné.
        
    model : str
        Le nom du modèle utilisé pour effectuer la prédiction.
    """
    prix_m2_estime: float
    ville_modele: str
    model: str
