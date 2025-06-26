from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

class PredictDirectRequest(BaseModel):
    surface_reelle_bati: float = Field(..., alias="Surface reelle bati")
    surface_terrain: float = Field(..., alias="Surface terrain")
    nombre_de_lots: float = Field(..., alias="Nombre de lots")
    type_local: Literal["Appartement", "Maison"] = Field(..., alias="Type local")

    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid"
    )


class PredictRequest(BaseModel):
    ville: str
    features: PredictDirectRequest


class PredictResponse(BaseModel):
    prix_m2_estime: float
    ville_modele: str
    model: str
