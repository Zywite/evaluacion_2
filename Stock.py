from Ingrediente import Ingrediente as AppIngrediente
from models import Ingrediente as OrmIngrediente
from typing import Dict, List
from database import get_db_session
from sqlalchemy.orm import Session
from decimal import Decimal

class Stock:
    def __init__(self):
        self.lista_ingredientes: Dict[str, AppIngrediente] = {}
        self._load_ingredients_from_db()

    def _load_ingredients_from_db(self):
        session: Session = get_db_session()
        try:
            ingredientes_db = session.query(OrmIngrediente).all()
            for ing_db in ingredientes_db:
                self.lista_ingredientes[ing_db.nombre] = AppIngrediente(
                    nombre=ing_db.nombre,
                    unidad=ing_db.unidad,
                    cantidad=ing_db.cantidad
                )
        finally:
            session.close()

    def agregar_ingrediente(self, ingrediente_app: AppIngrediente):
        session: Session = get_db_session()
        try:
            ing_existente_db = session.query(OrmIngrediente).filter_by(nombre=ingrediente_app.nombre).first()
            if ing_existente_db:
                ing_existente_db.cantidad += ingrediente_app.cantidad
                self.lista_ingredientes[ing_existente_db.nombre].cantidad = ing_existente_db.cantidad
            else:
                ing_orm = OrmIngrediente(
                    nombre=ingrediente_app.nombre,
                    unidad=ingrediente_app.unidad,
                    cantidad=ingrediente_app.cantidad
                )
                session.add(ing_orm)
                self.lista_ingredientes[ing_orm.nombre] = AppIngrediente(
                    nombre=ing_orm.nombre,
                    unidad=ing_orm.unidad,
                    cantidad=ing_orm.cantidad
                )
            session.commit()
        finally:
            session.close()

    def eliminar_ingrediente(self, nombre_ingrediente: str) -> bool:
        session: Session = get_db_session()
        try:
            ing_a_eliminar = session.query(OrmIngrediente).filter_by(nombre=nombre_ingrediente).first()
            if ing_a_eliminar:
                if nombre_ingrediente in self.lista_ingredientes:
                    del self.lista_ingredientes[nombre_ingrediente]
                session.delete(ing_a_eliminar)
                session.commit()
                return True
            return False
        finally:
            session.close()

    def verificar_stock(self) -> bool:
        return len(self.lista_ingredientes) > 0

    def verificar_ingredientes_suficientes(self, ingredientes_necesarios: List[AppIngrediente]) -> bool:
        for ing_necesario in ingredientes_necesarios:
            ing_stock = self.lista_ingredientes.get(ing_necesario.nombre)
            if ing_stock is None or ing_stock.cantidad < ing_necesario.cantidad:
                return False
        return True

    def reservar_ingredientes(self, ingredientes: List[AppIngrediente]):
        session: Session = get_db_session()
        try:
            for ing_necesario in ingredientes:
                ing_stock_db = session.query(OrmIngrediente).filter_by(nombre=ing_necesario.nombre).first()
                if ing_stock_db:
                    ing_stock_db.cantidad -= ing_necesario.cantidad
                    self.lista_ingredientes[ing_stock_db.nombre].cantidad = ing_stock_db.cantidad
            session.commit()
        finally:
            session.close()

    def devolver_ingredientes(self, ingredientes: List[AppIngrediente]):
        session: Session = get_db_session()
        try:
            for ing_devolver in ingredientes:
                ing_stock_db = session.query(OrmIngrediente).filter_by(nombre=ing_devolver.nombre).first()
                if ing_stock_db:
                    ing_stock_db.cantidad += ing_devolver.cantidad
                    self.lista_ingredientes[ing_stock_db.nombre].cantidad = ing_stock_db.cantidad
            session.commit()
        finally:
            session.close()

    def actualizar_stock(self, nombre_ingrediente: str, nueva_cantidad: float):
        session: Session = get_db_session()
        try:
            ing_a_actualizar = session.query(OrmIngrediente).filter_by(nombre=nombre_ingrediente).first()
            if ing_a_actualizar:
                dec_nueva_cantidad = Decimal(str(nueva_cantidad))
                ing_a_actualizar.cantidad = dec_nueva_cantidad
                self.lista_ingredientes[ing_a_actualizar.nombre].cantidad = dec_nueva_cantidad
                session.commit()
                return True
            return False
        finally:
            session.close()

    def obtener_elementos_menu(self) -> List[AppIngrediente]:
        return list(self.lista_ingredientes.values())