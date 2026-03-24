from pydantic import BaseModel
from typing import Literal

class AIResponse(BaseModel):
    sentimiento: Literal["positivo", "negativo", "neutro"]
    tema: Literal[
        "Servicio al Cliente",
        "Calidad del Producto",
        "Precio",
        "Limpieza",
        "Otro"
    ]
    resumen: str