from sqlalchemy.orm import Session, joinedload
from models import Menu, MenuIngrediente, Ingrediente
from sqlalchemy.exc import IntegrityError
from decimal import Decimal

def get_all_menus(session: Session):
    """
    Recupera todos los menús de la base de datos, incluyendo sus ingredientes.
    """
    return session.query(Menu).options(joinedload(Menu.ingredientes).joinedload(MenuIngrediente.ingrediente)).order_by(Menu.id).all()

def get_menu_by_name(session: Session, nombre: str):
    """
    Recupera un solo menú por su nombre.
    """
    return session.query(Menu).filter(Menu.nombre == nombre).first()

def create_menu(session: Session, nombre: str, precio: Decimal, icono_path: str, ingredientes: list):
    """
    Crea un nuevo menú en la base de datos.
    'ingredientes' debe ser una lista de diccionarios, cada uno con 'ingrediente_id' y 'cantidad_necesaria'.
    """
    try:
        nuevo_menu = Menu(nombre=nombre, precio=precio, icono_path=icono_path)
        session.add(nuevo_menu)
        session.flush()  # Realiza un 'flush' para obtener el ID del nuevo menú

        for ing_data in ingredientes:
            menu_ingrediente = MenuIngrediente(
                menu_id=nuevo_menu.id,
                ingrediente_id=ing_data['ingrediente_id'],
                cantidad_necesaria=ing_data['cantidad_necesaria']
            )
            session.add(menu_ingrediente)
        
        session.commit()
        return nuevo_menu
    except IntegrityError:
        session.rollback()
        raise

def update_menu(session: Session, menu_id: int, nombre: str, precio: Decimal, icono_path: str, ingredientes: list):
    """
    Actualiza la información de un menú existente.
    'ingredientes' debe ser una lista de diccionarios, cada uno con 'ingrediente_id' y 'cantidad_necesaria'.
    """
    menu = session.query(Menu).filter(Menu.id == menu_id).one()
    menu.nombre = nombre
    menu.precio = precio
    menu.icono_path = icono_path

    # Elimina los ingredientes antiguos
    session.query(MenuIngrediente).filter(MenuIngrediente.menu_id == menu_id).delete()

    # Agrega nuevos ingredientes
    for ing_data in ingredientes:
        menu_ingrediente = MenuIngrediente(
            menu_id=menu_id,
            ingrediente_id=ing_data['ingrediente_id'],
            cantidad_necesaria=ing_data['cantidad_necesaria']
        )
        session.add(menu_ingrediente)
    
    session.commit()
    return menu

def delete_menu(session: Session, menu_id: int):
    """
    Borra un menu de la base de datos.
    """
    menu = session.query(Menu).filter(Menu.id == menu_id).first()
    if menu:
        # Borra el manualmente debido problemas con cascade en la db
        session.query(MenuIngrediente).filter(MenuIngrediente.menu_id == menu_id).delete()
        session.delete(menu)
        session.commit()
        return True
    return False
