from Ingrediente import Ingrediente
from typing import Dict, List

class Stock:
    """
    Gestiona el inventario de ingredientes del restaurante.

    Decisión de Diseño: Se utiliza un diccionario (`Dict[str, Ingrediente]`) para almacenar
    los ingredientes. Esto garantiza un rendimiento óptimo (tiempo constante, O(1)) para
    operaciones clave como agregar, buscar, actualizar o eliminar ingredientes, sin importar
    cuán grande sea el inventario.
    """
    def __init__(self):
        self.lista_ingredientes: Dict[str, Ingrediente] = {}

    def agregar_ingrediente(self, ingrediente: Ingrediente):
        if ingrediente.nombre in self.lista_ingredientes:
            # Si ya existe, actualiza la cantidad
            ing_existente = self.lista_ingredientes[ingrediente.nombre]
            nueva_cantidad = ing_existente.cantidad + ingrediente.cantidad
            ing_existente.cantidad = round(nueva_cantidad, 1)
        else:
            # Si no existe, lo agrega al diccionario
            ingrediente.cantidad = round(ingrediente.cantidad, 1)
            self.lista_ingredientes[ingrediente.nombre] = ingrediente

    def eliminar_ingrediente(self, nombre_ingrediente):
        if nombre_ingrediente in self.lista_ingredientes:
            del self.lista_ingredientes[nombre_ingrediente]

    def verificar_stock(self):
        return len(self.lista_ingredientes) > 0

    def verificar_ingredientes_suficientes(self, ingredientes_necesarios: List[Ingrediente]) -> bool:
        for ing_necesario in ingredientes_necesarios:
            ing_stock = self.lista_ingredientes.get(ing_necesario.nombre)
            if ing_stock is None or ing_stock.cantidad < ing_necesario.cantidad:
                return False
        return True

    def reservar_ingredientes(self, ingredientes: List[Ingrediente]):
        """Resta los ingredientes del stock"""
        for ing_necesario in ingredientes:
            if ing_necesario.nombre in self.lista_ingredientes:
                ing_stock = self.lista_ingredientes[ing_necesario.nombre]
                nueva_cantidad = ing_stock.cantidad - ing_necesario.cantidad
                ing_stock.cantidad = round(nueva_cantidad, 1)

    def devolver_ingredientes(self, ingredientes: List[Ingrediente]):
        """Devuelve los ingredientes al stock"""
        for ing_devolver in ingredientes:
            if ing_devolver.nombre in self.lista_ingredientes:
                ing_stock = self.lista_ingredientes[ing_devolver.nombre]
                nueva_cantidad = ing_stock.cantidad + ing_devolver.cantidad
                ing_stock.cantidad = round(nueva_cantidad, 1)

    def actualizar_stock(self, nombre_ingrediente, nueva_cantidad):
        if nombre_ingrediente in self.lista_ingredientes:
            self.lista_ingredientes[nombre_ingrediente].cantidad = float(nueva_cantidad)
            return True
        return False

    def obtener_elementos_menu(self):
        return list(self.lista_ingredientes.values())
