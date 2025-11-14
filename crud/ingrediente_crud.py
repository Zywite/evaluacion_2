from sqlalchemy.orm import Session
from models import Ingrediente
from sqlalchemy.exc import IntegrityError
from decimal import Decimal

def get_all_ingredientes(session: Session):
    """
    Recupera todos los ingredientes de la base de datos.
    """
    return session.query(Ingrediente).order_by(Ingrediente.id).all()

def get_ingrediente_by_name(session: Session, nombre: str):
    """
    Recupera un solo ingrediente por su nombre.
    """
    return session.query(Ingrediente).filter(Ingrediente.nombre == nombre).first()

def create_ingrediente(session: Session, nombre: str, unidad: str, cantidad: Decimal):
    """
    Crea un nuevo ingrediente en la base de datos.
    Lanza IntegrityError si el nombre del ingrediente ya está registrado.
    """
    try:
        nuevo_ingrediente = Ingrediente(nombre=nombre, unidad=unidad, cantidad=cantidad)
        session.add(nuevo_ingrediente)
        session.commit()
        return nuevo_ingrediente
    except IntegrityError:
        session.rollback()
        raise

def update_ingrediente(session: Session, ingrediente_id: int, nombre: str, unidad: str, cantidad: Decimal):
    """
    Actualiza la información de un ingrediente existente.
    """
    ingrediente = session.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).one()
    ingrediente.nombre = nombre
    ingrediente.unidad = unidad
    ingrediente.cantidad = cantidad
    session.commit()
    return ingrediente

def delete_ingrediente(session: Session, nombre: str):
    """
    Elimina un ingrediente de la base de datos por su nombre.
    """
    ingrediente = session.query(Ingrediente).filter(Ingrediente.nombre == nombre).first()
    if ingrediente:
        session.delete(ingrediente)
        session.commit()
        return True
    return False
