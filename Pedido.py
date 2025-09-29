from ElementoMenu import CrearMenu 
class Pedido:
    def __init__(self):
        self.menus = []  # Lista para almacenar objetos de tipo CrearMenu

    def agregar_menu(self, menu: CrearMenu):
        """Agrega un menú al pedido. Si el menú ya existe, aumenta la cantidad en 1."""
        for menu_existente in self.menus:
            if menu_existente.nombre == menu.nombre:
                menu_existente.cantidad += 1  # Asume que CrearMenu tiene un atributo cantidad
                return
        # Si el menú no existe en el pedido, agregarlo
        menu.cantidad = 1  # Asigna 1 como cantidad inicial
        self.menus.append(menu)

    def eliminar_menu(self, nombre_menu: str):
        """Elimina un menú del pedido por su nombre."""
        self.menus = [menu for menu in self.menus if menu.nombre != nombre_menu]

    def mostrar_pedido(self):
        """Muestra todos los menús agregados al pedido."""
        for menu in self.menus:
            print(f"Nombre: {menu.nombre}, Cantidad: {menu.cantidad}, Precio: {menu.precio}")

    def calcular_total(self) -> float:
        """Calcula el precio total del pedido."""
        return sum(menu.precio * menu.cantidad for menu in self.menus)
