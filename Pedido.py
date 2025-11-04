from ElementoMenu import CrearMenu 
from typing import Dict, List, Tuple
from database import get_db_session
from models import Pedido as PedidoModel, PedidoItem, Menu
from sqlalchemy.orm import Session
import datetime

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
                nombre=existing_menu.nombre,
                ingredientes=existing_menu.ingredientes,
                precio=existing_menu.precio,
                icono_path=existing_menu.icono_path,
                cantidad=existing_menu.cantidad + 1
            )
        else:
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
                existing_menu = self.menus[nombre_menu]
                self.menus[nombre_menu] = CrearMenu(
                    nombre=existing_menu.nombre,
                    ingredientes=existing_menu.ingredientes,
                    precio=existing_menu.precio,
                    icono_path=existing_menu.icono_path,
                    cantidad=existing_menu.cantidad - 1
                )
            else:
                del self.menus[nombre_menu]

    def mostrar_pedido(self) -> List[Tuple[str, int, float]]:
        return [(menu.nombre, menu.cantidad, menu.precio) for menu in self.menus.values()]
   
    def calcular_total(self) -> float:
        return sum(menu.precio * menu.cantidad for menu in self.menus.values())

    def guardar_pedido(self):
        session: Session = get_db_session()
        try:
            total = self.calcular_total()
            
            nuevo_pedido = PedidoModel(total=total)
            session.add(nuevo_pedido)
            session.flush() # To get the new pedido's ID

            for menu_item in self.menus.values():
                menu_db = session.query(Menu).filter_by(nombre=menu_item.nombre).first()
                if menu_db:
                    nuevo_item = PedidoItem(
                        pedido_id=nuevo_pedido.id,
                        menu_id=menu_db.id,
                        cantidad=menu_item.cantidad,
                        precio_unitario=menu_item.precio
                    )
                    session.add(nuevo_item)
            
            session.commit()
            return nuevo_pedido.id
        finally:
            session.close()