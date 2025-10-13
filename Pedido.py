from ElementoMenu import CrearMenu 
from typing import Dict, List, Tuple

class Pedido:
    """
    Gestiona el estado del pedido actual de un cliente.

    Decisión de Diseño: Al igual que la clase Stock, utiliza un diccionario para almacenar
    los menús del pedido. La clave es el nombre del menú y el valor es el objeto CrearMenu.
    Esto permite agregar o eliminar menús de forma extremadamente eficiente (O(1)),
    lo que es crucial para una experiencia de usuario fluida.
    """
    def __init__(self):
        # Usar un diccionario para acceso O(1)
        self.menus: Dict[str, CrearMenu] = {}#se crea el diccionario vacio para el menu

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
            ) # incrementa la cantidad del menu en +1 o lo que s e el que se le indique
        else:
            # Si es nuevo, lo agregamos con cantidad 1
            self.menus[menu.nombre] = CrearMenu(
                nombre=menu.nombre,
                ingredientes=menu.ingredientes,
                precio=menu.precio,
                icono_path=menu.icono_path,
                cantidad=1
            ) # solo lo agrega si es nuevo nada mas

    def eliminar_menu(self, nombre_menu: str): # elimina lo que se indique del menu
        if nombre_menu in self.menus: # si esta en el diccionario
            if self.menus[nombre_menu].cantidad > 1: #si la cantidad es mayor de 1 lo decrementa
                existing_menu = self.menus[nombre_menu] # se guarda el menu en una variable
                self.menus[nombre_menu] = CrearMenu( 
                    nombre=existing_menu.nombre,
                    ingredientes=existing_menu.ingredientes,
                    precio=existing_menu.precio,
                    icono_path=existing_menu.icono_path,
                    cantidad=existing_menu.cantidad - 1
                ) # decrementa lo que se indique del menu solo 1
            else:
                del self.menus[nombre_menu] # si solo queda 1 lo elimina del todo

    def mostrar_pedido(self) -> List[Tuple[str, int, float]]: # muestra el pedido en una lista de tuplas
        return [(menu.nombre, menu.cantidad, menu.precio) for menu in self.menus.values()] 
        # retorna la lista de tuplas con el nombre, el precio, la cantidad del menu
   
    def calcular_total(self) -> float: # calcula el total del menu
        return sum(menu.precio * menu.cantidad for menu in self.menus.values())
        # retorna la multiplicacion del preciop por la cantidad pedida del menu
