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
        # Para una búsqueda eficiente, se convierte la lista de stock en un diccionario.
        # La clave puede ser el nombre del ingrediente o una tupla (nombre, unidad).
        # Aquí se usa solo el nombre para simplificar, asumiendo nombres únicos.
        stock_disponible = {ing.nombre: ing for ing in stock.lista_ingredientes}

        for ingrediente_requerido in self.ingredientes:
            # 1. Buscar el ingrediente en el stock
            ingrediente_en_stock = stock_disponible.get(ingrediente_requerido.nombre)

            # 2. Verificar si no existe o si la cantidad es insuficiente
            if (ingrediente_en_stock is None or 
                int(ingrediente_en_stock.cantidad) < int(ingrediente_requerido.cantidad)):
                return False
            
            # 3. (Opcional) Verificar si las unidades coinciden, si se especifica
            if (ingrediente_requerido.unidad is not None and 
                ingrediente_requerido.unidad != ingrediente_en_stock.unidad):
                return False

        return True
