from pydantic import BaseModel, Field
from typing import Literal, Optional, Dict, Any


class Features(BaseModel):
    surface_bati: float = Field(..., gt=0, description="Surface réelle bâtie (m²)")
    nombre_pieces: int = Field(..., gt=0, description="Nombre de pièces principales")
    type_local: Literal["Appartement", "Maison"]
    surface_terrain: Optional[float] = Field(0, ge=0, description="Surface terrain (m²)")
    nombre_lots: Optional[int] = Field(1, ge=1, description="Nombre de lots")

class PredictRequest(BaseModel): 
    ville: Optional[Literal["lille","bordeaux"]]
    Features: Optional[Features]

class PredictDirectRequest(Features):
    pass 

class PredictResponse(BaseModel):
    prix_m2_estime: float
    ville_modele: str
    model: str
