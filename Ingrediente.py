from dataclasses import dataclass
from typing import Optional
from decimal import Decimal

@dataclass(eq=True, frozen=False)
class Ingrediente:
    nombre: str
    unidad: Optional[str]  
    cantidad: Decimal          

    def __post_init__(self):
        # Ensure cantidad is always a Decimal
        if not isinstance(self.cantidad, Decimal):
            self.cantidad = Decimal(str(self.cantidad))

    def __str__(self):
        return f"{self.nombre} x {self.cantidad} {self.unidad}"