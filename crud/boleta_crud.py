"""
CRUD para la tabla boletas.

Proporciona operaciones de lectura/escritura para boletas generadas,
permitiendo auditoría y rastreo de boletas por pedido.
"""

from sqlalchemy.orm import Session
from models import Boleta
from decimal import Decimal
import datetime


def create_boleta(
    session: Session, 
    pedido_id: int, 
    subtotal: Decimal, 
    iva: Decimal, 
    total: Decimal, 
    pdf_path: str,
    estado: str = 'generada'
) -> Boleta:
    """
    Crea una nueva boleta en la base de datos.
    
    Args:
        session: Sesión de BD
        pedido_id: ID del pedido asociado
        subtotal: Subtotal (sin IVA)
        iva: Monto del IVA
        total: Total final
        pdf_path: Ruta del archivo PDF generado
        estado: Estado de la boleta (default: 'generada')
    
    Returns:
        Objeto Boleta creado
    """
    boleta = Boleta(
        pedido_id=pedido_id,
        fecha_generacion=datetime.datetime.utcnow(),
        subtotal=subtotal,
        iva=iva,
        total=total,
        pdf_path=pdf_path,
        estado=estado
    )
    session.add(boleta)
    session.commit()
    return boleta


def get_boleta_by_id(session: Session, boleta_id: int) -> Boleta:
    """
    Obtiene una boleta por su ID.
    
    Args:
        session: Sesión de BD
        boleta_id: ID de la boleta
    
    Returns:
        Objeto Boleta o None si no existe
    """
    return session.query(Boleta).filter(Boleta.id == boleta_id).first()


def get_boleta_by_pedido_id(session: Session, pedido_id: int) -> Boleta:
    """
    Obtiene la boleta asociada a un pedido.
    
    Args:
        session: Sesión de BD
        pedido_id: ID del pedido
    
    Returns:
        Objeto Boleta o None si no existe
    """
    return session.query(Boleta).filter(Boleta.pedido_id == pedido_id).first()


def get_all_boletas(session: Session, estado: str = None) -> list:
    """
    Obtiene todas las boletas, opcionalmente filtradas por estado.
    
    Args:
        session: Sesión de BD
        estado: Estado de la boleta (opcional, e.g., 'generada', 'anulada')
    
    Returns:
        Lista de objetos Boleta
    """
    query = session.query(Boleta).order_by(Boleta.fecha_generacion.desc())
    
    if estado:
        query = query.filter(Boleta.estado == estado)
    
    return query.all()


def update_boleta_pdf_path(session: Session, boleta_id: int, pdf_path: str) -> Boleta:
    """
    Actualiza la ruta del PDF de una boleta (en caso de regeneración).
    
    Args:
        session: Sesión de BD
        boleta_id: ID de la boleta
        pdf_path: Nueva ruta del PDF
    
    Returns:
        Objeto Boleta actualizado
    """
    boleta = session.query(Boleta).filter(Boleta.id == boleta_id).first()
    if boleta:
        boleta.pdf_path = pdf_path
        session.commit()
    return boleta


def update_boleta_estado(session: Session, boleta_id: int, estado: str) -> Boleta:
    """
    Actualiza el estado de una boleta (e.g., 'generada' -> 'anulada').
    
    Args:
        session: Sesión de BD
        boleta_id: ID de la boleta
        estado: Nuevo estado
    
    Returns:
        Objeto Boleta actualizado
    """
    boleta = session.query(Boleta).filter(Boleta.id == boleta_id).first()
    if boleta:
        boleta.estado = estado
        session.commit()
    return boleta


def delete_boleta(session: Session, boleta_id: int) -> bool:
    """
    Elimina una boleta de la base de datos.
    
    Args:
        session: Sesión de BD
        boleta_id: ID de la boleta a eliminar
    
    Returns:
        True si se eliminó, False si no existía
    """
    boleta = session.query(Boleta).filter(Boleta.id == boleta_id).first()
    if boleta:
        session.delete(boleta)
        session.commit()
        return True
    return False


def count_boletas_by_estado(session: Session, estado: str) -> int:
    """
    Cuenta el número de boletas con un estado específico.
    
    Args:
        session: Sesión de BD
        estado: Estado a contar
    
    Returns:
        Cantidad de boletas
    """
    return session.query(Boleta).filter(Boleta.estado == estado).count()
