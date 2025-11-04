# IMenu.py
from typing import Protocol, List, Optional
from Ingrediente import Ingrediente
from Stock import Stock
from decimal import Decimal

class IMenu(Protocol):
    """Interfaz para los elementos del menú."""
    nombre: str
    ingredientes: List[Ingrediente]
    precio: Decimal
    cantidad: int
    icono_path: Optional[str]
    
    def esta_disponible(self, stock: Stock) -> bool:
        ...