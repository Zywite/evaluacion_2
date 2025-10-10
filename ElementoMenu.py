from dataclasses import dataclass, field
from typing import List, Optional
from Ingrediente import Ingrediente
from Stock import Stock
from IMenu import IMenu

@dataclass(frozen=True)
class CrearMenu(IMenu):
    nombre: str
    ingredientes: List[Ingrediente] = field(hash=False, compare=False)
    precio: float = field(default=0.0, compare=False)
    icono_path: Optional[str] = field(default=None, compare=False)
    cantidad: int = field(default=0, compare=False)

    def __hash__(self):
        return hash(self.nombre)

    def esta_disponible(self, stock: Stock) -> bool:
        for req in self.ingredientes:
            ok = False
            for ing in stock.lista_ingredientes:
                if ing.nombre == req.nombre and (req.unidad is None or ing.unidad == req.unidad):
                    if int(ing.cantidad) >= int(req.cantidad):
                        ok = True
                        break
            if not ok:
                return False
        return True

