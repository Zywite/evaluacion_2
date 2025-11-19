from __future__ import annotations
from sqlalchemy import String, DECIMAL, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from decimal import Decimal
import datetime
from typing import TYPE_CHECKING, List

Base = declarative_base()

if TYPE_CHECKING:
    pass

class Cliente(Base):
    __tablename__ = 'clientes'
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(191), unique=True, nullable=False)
    pedidos: Mapped[List[Pedido]] = relationship(back_populates="cliente")

class Ingrediente(Base):
    __tablename__ = 'ingredientes'
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(191), unique=True)
    unidad: Mapped[str] = mapped_column(String(50))
    cantidad: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))

class Menu(Base):
    __tablename__ = 'menus'
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(191), unique=True)
    precio: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    icono_path: Mapped[str] = mapped_column(String(255), nullable=True)
    ingredientes: Mapped[List[MenuIngrediente]] = relationship(back_populates="menu")

class MenuIngrediente(Base):
    __tablename__ = 'menu_ingredientes'
    menu_id: Mapped[int] = mapped_column(ForeignKey('menus.id'), primary_key=True)
    ingrediente_id: Mapped[int] = mapped_column(ForeignKey('ingredientes.id', ondelete="CASCADE"), primary_key=True)
    cantidad_necesaria: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    menu: Mapped[Menu] = relationship(back_populates="ingredientes")
    ingrediente: Mapped[Ingrediente] = relationship()

class Pedido(Base):
    __tablename__ = 'pedidos'
    id: Mapped[int] = mapped_column(primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey('clientes.id'))
    fecha: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    estado: Mapped[str] = mapped_column(String(50), default='pendiente')
    tipo_entrega: Mapped[str] = mapped_column(String(50))
    total: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    cliente: Mapped[Cliente] = relationship(back_populates="pedidos")
    items: Mapped[List[PedidoItem]] = relationship(back_populates="pedido")

class PedidoItem(Base):
    __tablename__ = 'pedido_items'
    id: Mapped[int] = mapped_column(primary_key=True)
    pedido_id: Mapped[int] = mapped_column(ForeignKey('pedidos.id'))
    menu_id: Mapped[int] = mapped_column(ForeignKey('menus.id'))
    cantidad: Mapped[int]
    precio_unitario: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    subtotal: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    pedido: Mapped[Pedido] = relationship(back_populates="items")
    menu: Mapped[Menu] = relationship()

class Boleta(Base):
    """
    Modelo para almacenar información de boletas generadas.
    
    Relación 1:1 con Pedido (cada pedido tiene una boleta).
    Almacena los datos calculados (subtotal, IVA) y la ruta del PDF
    para referencia y auditoría.
    """
    __tablename__ = 'boletas'
    id: Mapped[int] = mapped_column(primary_key=True)
    pedido_id: Mapped[int] = mapped_column(ForeignKey('pedidos.id'), unique=True)
    fecha_generacion: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    subtotal: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    iva: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    total: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    pdf_path: Mapped[str] = mapped_column(String(255))
    estado: Mapped[str] = mapped_column(String(50), default='generada')  # generada, anulada, etc.
    pedido: Mapped[Pedido] = relationship()