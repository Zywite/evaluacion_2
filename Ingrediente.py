# Ingrediente.py
from dataclasses import dataclass
from typing import Optional

@dataclass(eq=True, frozen=False)
class Ingrediente:
    nombre: str
    unidad: Optional[str]   # <-- va 2° (sin valor por defecto)
    cantidad: float           # <-- va 3°

    def __post_init__(self):
        # Normalizamos cantidad a int siempre
        self.cantidad = float(self.cantidad)

    def __str__(self):
        if self.unidad:
            return f"{self.nombre} ({self.unidad}) x {self.cantidad}"
        return f"{self.nombre} x {self.cantidad}"