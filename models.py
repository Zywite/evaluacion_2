from sqlalchemy import String, DECIMAL, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from decimal import Decimal
import datetime
from typing import List

Base = declarative_base()

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
    ingredientes: Mapped[List["MenuIngrediente"]] = relationship(back_populates="menu")

class MenuIngrediente(Base):
    __tablename__ = 'menu_ingredientes'
    menu_id: Mapped[int] = mapped_column(ForeignKey('menus.id'), primary_key=True)
    ingrediente_id: Mapped[int] = mapped_column(ForeignKey('ingredientes.id', ondelete="CASCADE"), primary_key=True)
    cantidad_necesaria: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    menu: Mapped["Menu"] = relationship(back_populates="ingredientes")
    ingrediente: Mapped["Ingrediente"] = relationship()

class Pedido(Base):
    __tablename__ = 'pedidos'
    id: Mapped[int] = mapped_column(primary_key=True)
    fecha: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    total: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    items: Mapped[List["PedidoItem"]] = relationship(back_populates="pedido")

class PedidoItem(Base):
    __tablename__ = 'pedido_items'
    id: Mapped[int] = mapped_column(primary_key=True)
    pedido_id: Mapped[int] = mapped_column(ForeignKey('pedidos.id'))
    menu_id: Mapped[int] = mapped_column(ForeignKey('menus.id'))
    cantidad: Mapped[int]
    precio_unitario: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    pedido: Mapped["Pedido"] = relationship(back_populates="items")
    menu: Mapped["Menu"] = relationship()