from ElementoMenu import CrearMenu 
class Pedido:
    def __init__(self):
        self.menus = []  

    def agregar_menu(self, menu: CrearMenu):
        # Buscar si el menú ya existe en el pedido
        for m in self.menus:
            if m.nombre == menu.nombre:
                # Crear un nuevo menú con la cantidad incrementada
                nuevo_menu = CrearMenu(
                    nombre=m.nombre,
                    ingredientes=m.ingredientes,
                    precio=m.precio,
                    icono_path=m.icono_path,
                    cantidad=m.cantidad + 1
                )
                # Reemplazar el menú existente
                self.menus[self.menus.index(m)] = nuevo_menu
                return
        
        # Si no existe, agregar como nuevo con cantidad 1
        menu_copy = CrearMenu(
            nombre=menu.nombre,
            ingredientes=menu.ingredientes.copy(),
            precio=menu.precio,
            icono_path=menu.icono_path,
            cantidad=1
        )
        self.menus.append(menu_copy)

    def eliminar_menu(self, nombre_menu: str):
        for i, menu in enumerate(self.menus):
            if menu.nombre == nombre_menu:
                if menu.cantidad > 1:
                    # Crear un nuevo menú con la cantidad decrementada
                    nuevo_menu = CrearMenu(
                        nombre=menu.nombre,
                        ingredientes=menu.ingredientes,
                        precio=menu.precio,
                        icono_path=menu.icono_path,
                        cantidad=menu.cantidad - 1
                    )
                    self.menus[i] = nuevo_menu
                else:
                    # Si la cantidad es 1, eliminar el menú
                    self.menus.pop(i)
                break

    def mostrar_pedido(self):
        return [(menu.nombre, menu.cantidad, menu.precio) for menu in self.menus]

    def calcular_total(self) -> float:
        return sum(menu.precio * menu.cantidad for menu in self.menus)
