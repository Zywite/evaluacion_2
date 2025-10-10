# Ingrediente.py
from dataclasses import dataclass
from typing import Optional

@dataclass(eq=True, frozen=False)
class Ingrediente:
    nombre: str
    unidad: Optional[str]  
    cantidad: float          

    def __post_init__(self):
        self.cantidad = round(float(self.cantidad), 1)

    def __str__(self):
        return f"{self.nombre} x {self.cantidad} {self.unidad}"