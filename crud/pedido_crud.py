from sqlalchemy.orm import Session, joinedload
from models import Pedido, PedidoItem
import datetime
from decimal import Decimal

def get_all_pedidos(session: Session):
    """
    Recupera todos los pedidos de la base de datos.
    """
    return session.query(Pedido).options(joinedload(Pedido.cliente), joinedload(Pedido.items).joinedload(PedidoItem.menu)).order_by(Pedido.fecha.desc()).all()

def get_pedido_by_id(session: Session, pedido_id: int):
    """
    Recupera un solo pedido por su ID, incluyendo el cliente y los ítems relacionados.
    """
    return session.query(Pedido).options(joinedload(Pedido.cliente), joinedload(Pedido.items).joinedload(PedidoItem.menu)).filter(Pedido.id == pedido_id).first()

def create_pedido(session: Session, cliente_id: int, items: list, estado: str = 'completado', tipo_entrega: str = 'local'):
    """
    'items' debe ser una lista de diccionarios, cada uno con 'menu_id', 'cantidad' y 'precio_unitario'.
    """
    total = sum(Decimal(item['cantidad']) * Decimal(item['precio_unitario']) for item in items)
    
    nuevo_pedido = Pedido(
        cliente_id=cliente_id,
        fecha=datetime.datetime.utcnow(),
        estado=estado,
        tipo_entrega=tipo_entrega,
        total=total
    )
    session.add(nuevo_pedido)
    session.flush()  # Realiza un 'flush' para obtener el ID del nuevo pedido

    for item_data in items:
        # Calculate subtotal for the PedidoItem
        item_subtotal = Decimal(item_data['cantidad']) * Decimal(item_data['precio_unitario'])
        pedido_item = PedidoItem(
            pedido_id=nuevo_pedido.id,
            menu_id=item_data['menu_id'],
            cantidad=item_data['cantidad'],
            precio_unitario=item_data['precio_unitario'],
            subtotal=item_subtotal # Add the subtotal here
        )
        session.add(pedido_item)
    
    session.commit()
    return nuevo_pedido

def delete_pedido(session: Session, pedido_id: int):
    """
    Elimina un pedido de la base de datos.
    """
    pedido = session.query(Pedido).filter(Pedido.id == pedido_id).first()
    if pedido:
        # Eliminar manualmente los ítems primero debido a problemas de cascada en algunas bases de datos.
        session.query(PedidoItem).filter(PedidoItem.pedido_id == pedido_id).delete()
        session.delete(pedido)
        session.commit()
        return True
    return False
