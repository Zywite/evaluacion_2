from ElementoMenu import CrearMenu 
from typing import Dict, List, Tuple

class Pedido:
    def __init__(self):
        # Usar un diccionario para acceso O(1)
        self.menus: Dict[str, CrearMenu] = {}

    def agregar_menu(self, menu: CrearMenu):
        if menu.nombre in self.menus:
            # Si el menú ya existe, simplemente incrementa su cantidad
            existing_menu = self.menus[menu.nombre]
            # dataclasses(frozen=True) son inmutables. Creamos una nueva instancia.
            self.menus[menu.nombre] = CrearMenu(
                nombre=existing_menu.nombre,
                ingredientes=existing_menu.ingredientes,
                precio=existing_menu.precio,
                icono_path=existing_menu.icono_path,
                cantidad=existing_menu.cantidad + 1
            )
        else:
            # Si es nuevo, lo agregamos con cantidad 1
            self.menus[menu.nombre] = CrearMenu(
                nombre=menu.nombre,
                ingredientes=menu.ingredientes,
                precio=menu.precio,
                icono_path=menu.icono_path,
                cantidad=1
            )

    def eliminar_menu(self, nombre_menu: str):
        if nombre_menu in self.menus:
            if self.menus[nombre_menu].cantidad > 1:
                # Si hay más de uno, decrementa la cantidad
                existing_menu = self.menus[nombre_menu]
                self.menus[nombre_menu] = CrearMenu(
                    nombre=existing_menu.nombre,
                    ingredientes=existing_menu.ingredientes,
                    precio=existing_menu.precio,
                    icono_path=existing_menu.icono_path,
                    cantidad=existing_menu.cantidad - 1
                )
            else:
                # Si solo queda uno, elimínalo del diccionario
                del self.menus[nombre_menu]

    def mostrar_pedido(self) -> List[Tuple[str, int, float]]:
        return [(menu.nombre, menu.cantidad, menu.precio) for menu in self.menus.values()]

    def calcular_total(self) -> float:
        return sum(menu.precio * menu.cantidad for menu in self.menus.values())
