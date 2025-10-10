class Stock:
    def __init__(self):
        self.lista_ingredientes = []

    def agregar_ingrediente(self, ingrediente):
        # Buscar si ya existe el ingrediente
        for i, ing in enumerate(self.lista_ingredientes):
            if ing.nombre == ingrediente.nombre:
                # Actualizar cantidad si existe, formateando a un decimal
                nueva_cantidad = float(self.lista_ingredientes[i].cantidad) + float(ingrediente.cantidad)
                self.lista_ingredientes[i].cantidad = round(nueva_cantidad, 1)
                return
        # Si no existe, agregar nuevo con cantidad formateada
        ingrediente.cantidad = round(float(ingrediente.cantidad), 1)
        self.lista_ingredientes.append(ingrediente)

    def eliminar_ingrediente(self, nombre_ingrediente):
        self.lista_ingredientes = [ing for ing in self.lista_ingredientes if ing.nombre != nombre_ingrediente]

    def verificar_stock(self):
        return len(self.lista_ingredientes) > 0

    def verificar_ingredientes_suficientes(self, ingredientes_necesarios):
        if not self.lista_ingredientes:
            return False
            
        for ing_necesario in ingredientes_necesarios:
            encontrado = False
            for ing_stock in self.lista_ingredientes:
                if ing_necesario.nombre == ing_stock.nombre:
                    encontrado = True
                    if float(ing_stock.cantidad) < float(ing_necesario.cantidad):
                        return False
                    break
            if not encontrado:
                return False
        return True

    def reservar_ingredientes(self, ingredientes):
        """Resta los ingredientes del stock"""
        for ing_necesario in ingredientes:
            for ing_stock in self.lista_ingredientes:
                if ing_necesario.nombre == ing_stock.nombre:
                    nueva_cantidad = float(ing_stock.cantidad) - float(ing_necesario.cantidad)
                    ing_stock.cantidad = round(nueva_cantidad, 1)
                    break

    def devolver_ingredientes(self, ingredientes):
        """Devuelve los ingredientes al stock"""
        for ing_devolver in ingredientes:
            for ing_stock in self.lista_ingredientes:
                if ing_devolver.nombre == ing_stock.nombre:
                    nueva_cantidad = float(ing_stock.cantidad) + float(ing_devolver.cantidad)
                    ing_stock.cantidad = round(nueva_cantidad, 1)
                    break

    def actualizar_stock(self, nombre_ingrediente, nueva_cantidad):
        for ingrediente in self.lista_ingredientes:
            if ingrediente.nombre == nombre_ingrediente:
                ingrediente.cantidad = float(nueva_cantidad)
                return True
        return False

    def obtener_elementos_menu(self):
        return self.lista_ingredientes

