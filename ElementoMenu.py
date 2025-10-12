from dataclasses import dataclass, field
from typing import List, Optional
from Ingrediente import Ingrediente
from Stock import Stock
from IMenu import IMenu

@dataclass(frozen=True)
class CrearMenu(IMenu):
    """
    Implementación de un elemento del menú usando un dataclass inmutable.
    'frozen=True' garantiza que una vez creado, un objeto de menú no puede ser modificado,
    lo que previene errores al obligar a crear nuevas instancias para cualquier cambio (ej. al cambiar la cantidad en un pedido).
    """
    nombre: str
    ingredientes: List[Ingrediente] = field(hash=False, compare=False)
    precio: float = field(default=0.0, compare=False)
    icono_path: Optional[str] = field(default=None, compare=False)
    cantidad: int = field(default=0, compare=False)

    def __hash__(self):
        return hash(self.nombre)

    def esta_disponible(self, stock: Stock) -> bool:
        """
        Verifica si hay suficientes ingredientes en el stock para preparar este menú.
        Esta operación es muy eficiente gracias a que la clase Stock utiliza un diccionario
        para el inventario, permitiendo búsquedas de ingredientes en tiempo constante (O(1)).
        """
        # El inventario de stock ya es un diccionario optimizado para búsquedas rápidas.
        stock_disponible = stock.lista_ingredientes
        
        for ingrediente_requerido in self.ingredientes:
            # 1. Buscar el ingrediente en el stock
            ingrediente_en_stock = stock_disponible.get(ingrediente_requerido.nombre)

            # 2. Verificar si no existe o si la cantidad es insuficiente
            if (ingrediente_en_stock is None or 
                int(ingrediente_en_stock.cantidad) < int(ingrediente_requerido.cantidad)):
                return False
            
            # 3. Opcional: Verificar si las unidades coinciden, si se especifica.
            if (ingrediente_requerido.unidad is not None and 
                ingrediente_requerido.unidad != ingrediente_en_stock.unidad):
                return False

        return True
