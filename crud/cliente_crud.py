from sqlalchemy.orm import Session
from models import Cliente, Pedido as PedidoModel
from sqlalchemy.exc import IntegrityError

def get_all_clientes(session: Session):
    """
    Recupera todos los clientes de la base de datos.
    """
    return session.query(Cliente).order_by(Cliente.id).all()

def get_cliente_by_id(session: Session, cliente_id: int):
    """
    Recupera un solo cliente por su ID.
    """
    return session.query(Cliente).filter(Cliente.id == cliente_id).first()

def create_cliente(session: Session, nombre: str, apellido: str, email: str):
    """
    Crea un nuevo cliente en la base de datos.
    Lanza IntegrityError si el correo electrónico ya está registrado.
    """
    try:
        nuevo_cliente = Cliente(nombre=nombre, apellido=apellido, email=email)
        session.add(nuevo_cliente)
        session.commit()
        return nuevo_cliente
    except IntegrityError:
        session.rollback()
        raise

def update_cliente(session: Session, cliente_id: int, nombre: str, apellido: str, email: str):
    """
    Actualiza la información de un cliente existente.
    Lanza IntegrityError si el nuevo correo electrónico ya está registrado por otro cliente.
    """
    try:
        cliente = session.query(Cliente).filter(Cliente.id == cliente_id).one()
        cliente.nombre = nombre
        cliente.apellido = apellido
        cliente.email = email
        session.commit()
        return cliente
    except IntegrityError:
        session.rollback()
        raise

def delete_cliente(session: Session, cliente_id: int):
    """
    Elimina un cliente de la base de datos.
    Devuelve False si el cliente tiene pedidos asociados, True en caso contrario.
    """
    # Verifica si hay pedidos asociados
    pedidos_asociados = session.query(PedidoModel).filter(PedidoModel.cliente_id == cliente_id).count()
    if pedidos_asociados > 0:
        return False

    cliente = session.query(Cliente).filter(Cliente.id == cliente_id).one()
    session.delete(cliente)
    session.commit()
    return True
