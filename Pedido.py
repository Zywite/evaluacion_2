from ElementoMenu import CrearMenu 
from typing import Dict, List, Tuple

class Pedido:
    """
    Gestiona el estado del pedido actual de un cliente.
    """
    def __init__(self):
        self.menus: Dict[str, CrearMenu] = {}

    def agregar_menu(self, menu: CrearMenu):
        if menu.nombre in self.menus:
            existing_menu = self.menus[menu.nombre]
            self.menus[menu.nombre] = CrearMenu(
                id=existing_menu.id,
                nombre=existing_menu.nombre,
                ingredientes=existing_menu.ingredientes,
                precio=existing_menu.precio,
                icono_path=existing_menu.icono_path,
                cantidad=existing_menu.cantidad + 1
            )
        else:
            self.menus[menu.nombre] = CrearMenu(
                id=menu.id,
                nombre=menu.nombre,
                ingredientes=menu.ingredientes,
                precio=menu.precio,
                icono_path=menu.icono_path,
                cantidad=1
            )

    def eliminar_menu(self, nombre_menu: str):
        if nombre_menu in self.menus:
            if self.menus[nombre_menu].cantidad > 1:
                existing_menu = self.menus[nombre_menu]
                self.menus[nombre_menu] = CrearMenu(
                    id=existing_menu.id,
                    nombre=existing_menu.nombre,
                    ingredientes=existing_menu.ingredientes,
                    precio=existing_menu.precio,
                    icono_path=existing_menu.icono_path,
                    cantidad=existing_menu.cantidad - 1
                )
            else:
                del self.menus[nombre_menu]

    def mostrar_pedido(self) -> List[Tuple[str, int, float]]:
        return [(menu.nombre, menu.cantidad, float(menu.precio)) for menu in self.menus.values()]
   
    def calcular_total(self) -> float:
        total = sum(menu.precio * menu.cantidad for menu in self.menus.values())
        return float(total) if total else 0.0
