from typing import List
from ElementoMenu import CrearMenu
from Ingrediente import Ingrediente as AppIngrediente # Renaming to avoid conflict
from IMenu import IMenu
from database import get_db_session
from models import Menu, Ingrediente, MenuIngrediente
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from decimal import Decimal

def get_default_menus() -> List[IMenu]:
    menus_app: List[IMenu] = []
    session: Session = get_db_session()
    try:
        menus_db = session.query(Menu).options(joinedload(Menu.ingredientes).joinedload(MenuIngrediente.ingrediente)).all()
        for menu_db in menus_db:
            ingredientes_app = []
            for menu_ing in menu_db.ingredientes:
                ing_db = menu_ing.ingrediente
                ingredientes_app.append(
                    AppIngrediente(nombre=ing_db.nombre, unidad=ing_db.unidad, cantidad=menu_ing.cantidad_necesaria)
                )
            menus_app.append(
                CrearMenu(menu_db.nombre, ingredientes_app, menu_db.precio, menu_db.icono_path)
            )
    finally:
        session.close()
    return menus_app

def save_default_menus_to_db():
    session: Session = get_db_session()
    try:
        default_menus_data = [
            {
                "nombre": "Papas Fritas",
                "precio": Decimal("500"),
                "icono_path": "IMG/papas.png",
                "ingredientes": [("Papas", "unid", Decimal("2.0"))]
            },
            {
                "nombre": "Pepsi",
                "precio": Decimal("1100"),
                "icono_path": "IMG/bebida.png",
                "ingredientes": [("Pepsi", "unid", Decimal("1.0"))]
            },
            {
                "nombre": "Completo",
                "precio": Decimal("1800"),
                "icono_path": "IMG/completo.png",
                "ingredientes": [("Vienesa", "unid", Decimal("1.0")), ("Pan de completo", "unid", Decimal("1.0")), ("Tomate", "unid", Decimal("1.0")), ("Palta", "unid", Decimal("1.0"))]
            },
            {
                "nombre": "Hamburguesa",
                "precio": Decimal("3500"),
                "icono_path": "IMG/hamburguesa.png",
                "ingredientes": [("Pan de hamburguesa", "unid", Decimal("1.0")), ("Lamina de queso", "unid", Decimal("1.0")), ("Churrasco de carne", "unid", Decimal("1.0"))]
            },
            {
                "nombre": "Panqueques",
                "precio": Decimal("2000"),
                "icono_path": "IMG/panqueque.png",
                "ingredientes": [("Panqueques", "unid", Decimal("2.0")), ("Manjar", "unid", Decimal("1.0")), ("Azúcar flor", "unid", Decimal("1.0"))]
            },
            {
                "nombre": "Pollo Frito",
                "precio": Decimal("2800"),
                "icono_path": "IMG/pollo.png",
                "ingredientes": [("Presa de pollo", "unid", Decimal("1.0")), ("Harina", "unid", Decimal("2.0")), ("Aceite", "unid", Decimal("1.0"))]
            },
            {
                "nombre": "Ensalada Mixta",
                "precio": Decimal("1500"),
                "icono_path": "IMG/ensalada.png",
                "ingredientes": [("Lechuga", "unid", Decimal("1.0")), ("Tomate", "unid", Decimal("1.0")), ("Zanahoria", "unid", Decimal("1.0"))]
            },
        ]

        for menu_data in default_menus_data:
            menu_db = session.query(Menu).filter_by(nombre=menu_data["nombre"]).first()
            if not menu_db:
                menu_db = Menu(
                    nombre=menu_data["nombre"],
                    precio=menu_data["precio"],
                    icono_path=menu_data["icono_path"]
                )
                session.add(menu_db)
                session.flush()

            for ing_nombre, ing_unidad, ing_cantidad_necesaria in menu_data["ingredientes"]:
                ing_db = session.query(Ingrediente).filter_by(nombre=ing_nombre).first()
                if not ing_db:
                    ing_db = Ingrediente(nombre=ing_nombre, unidad=ing_unidad, cantidad=Decimal('0'))
                    session.add(ing_db)
                    session.flush()

                menu_ing_db = session.query(MenuIngrediente).filter_by(menu_id=menu_db.id, ingrediente_id=ing_db.id).first()
                if not menu_ing_db:
                    menu_ing_db = MenuIngrediente(
                        menu_id=menu_db.id,
                        ingrediente_id=ing_db.id,
                        cantidad_necesaria=ing_cantidad_necesaria
                    )
                    session.add(menu_ing_db)
        
        session.commit()
    except IntegrityError:
        session.rollback()
        print("Data already seeded or integrity error.")
    finally:
        session.close()