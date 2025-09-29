from Ingrediente import Ingrediente

class Stock:
    def __init__(self):
        self.lista_ingredientes = []

    def agregar_ingrediente(self, ingrediente):
        """
        Agrega un ingrediente a la lista de ingredientes.

        Parámetros:
        ingrediente (objeto): El ingrediente que se desea agregar. Se asume que el objeto tiene atributos 'nombre', 'cantidad' y 'unidad'.

        Descripción:
        Este método verifica si el ingrediente ya existe en la lista de ingredientes (`self.lista_ingredientes`).
        Si el ingrediente ya existe y la unidad es la misma, actualiza la cantidad del ingrediente existente sumando la cantidad del nuevo ingrediente.
        Si el ingrediente existe pero la unidad es diferente, muestra un mensaje de advertencia y no suma.
        Si el ingrediente no existe, lo agrega a la lista.

        Ejemplo de uso:
        >>> nuevo_ingrediente = Ingrediente(nombre="Azúcar", cantidad="100", unidad="g")
        >>> stock.agregar_ingrediente(nuevo_ingrediente)
        """
        for ing in self.lista_ingredientes:
            if ing.nombre == ingrediente.nombre:
                if hasattr(ing, "unidad") and hasattr(ingrediente, "unidad"):
                    if ing.unidad == ingrediente.unidad:
                        ing.cantidad = str(int(ing.cantidad) + int(ingrediente.cantidad))
                    else:
                        print(f"Advertencia: Las unidades no coinciden para '{ing.nombre}' ({ing.unidad} vs {ingrediente.unidad}). No se suma la cantidad.")
                    return
                else:
                    # Si no hay atributo unidad, se comporta como antes
                    ing.cantidad = str(int(ing.cantidad) + int(ingrediente.cantidad))
                    return

        # Si no existe, agregar como nuevo
        self.lista_ingredientes.append(ingrediente)

    def eliminar_ingrediente(self, nombre_ingrediente):
        """
        Elimina un ingrediente de la lista de ingredientes.

        Parámetros:
        nombre_ingrediente (str): El nombre del ingrediente que se desea eliminar.

        Descripción:
        Este método recorre la lista de ingredientes (`self.lista_ingredientes`) y busca un ingrediente cuyo nombre coincida con `nombre_ingrediente`.
        Si encuentra el ingrediente, lo elimina de la lista.

        Ejemplo de uso:
        stock.eliminar_ingrediente("Azúcar")
        """
        for ingrediente in self.lista_ingredientes:
            if ingrediente.nombre == nombre_ingrediente:
                self.lista_ingredientes.remove(ingrediente)
                break

    def verificar_stock(self):
        return len(self.lista_ingredientes)

    def actualizar_stock(self, nombre_ingrediente, nueva_cantidad):
        for ingrediente in self.lista_ingredientes:
            if ingrediente.nombre == nombre_ingrediente:
                ingrediente.cantidad = nueva_cantidad
                break

    def obtener_elementos_menu(self):
        return [elemento for elemento in self.lista_ingredientes]

