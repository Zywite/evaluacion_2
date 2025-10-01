from Ingrediente import Ingrediente

class Stock:
    def __init__(self):
        self.lista_ingredientes = []

    def agregar_ingrediente(self, ingrediente):

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

