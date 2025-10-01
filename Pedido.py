from ElementoMenu import CrearMenu 
class Pedido:
    def __init__(self):
        self.menus = []  

    def agregar_menu(self, menu: CrearMenu):

        for menu_existente in self.menus:
            if menu_existente.nombre == menu.nombre:
                menu_existente.cantidad += 1  
                return
        menu.cantidad = 1  
        self.menus.append(menu)

    def eliminar_menu(self, nombre_menu: str):

        self.menus = [menu for menu in self.menus if menu.nombre != nombre_menu]

    def mostrar_pedido(self):

        for menu in self.menus:
            print(f"Nombre: {menu.nombre}, Cantidad: {menu.cantidad}, Precio: {menu.precio}")

    def calcular_total(self) -> float:

        return sum(menu.precio * menu.cantidad for menu in self.menus)
