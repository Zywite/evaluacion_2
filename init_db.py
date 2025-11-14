from database import engine, Base, get_db_session
from models import Ingrediente, Menu, MenuIngrediente, Cliente, Pedido, PedidoItem
from datetime import datetime, timedelta
from decimal import Decimal
import os
import random
from random import randint

def reset_database():
    """Dropea la tabla y vuelve a crearla."""
    print("ADVERTENCIA: Esto eliminará todos los datos de la base de datos.")
    # Descomenta la siguiente línea si estás seguro de que quieres continuar
    input("Presiona Enter para continuar o Ctrl+C para cancelar.")
    
    print("Eliminando todas las tablas...")
    Base.metadata.drop_all(bind=engine)
    print("Tablas eliminadas.")
    
    print("Creando todas las tablas...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente.")

def populate_database():
    """Agrega datos iniciales a la base de datos."""
    session = get_db_session()
    print("Poblando la base de datos con datos iniciales...")

    try:
        # --- Ingredientes ---
        ingredientes = [
            Ingrediente(nombre='Pan de completo', unidad='unid', cantidad=Decimal('100')),
            Ingrediente(nombre='Vienesa', unidad='unid', cantidad=Decimal('100')),
            Ingrediente(nombre='Tomate', unidad='kg', cantidad=Decimal('10')),
            Ingrediente(nombre='Palta', unidad='kg', cantidad=Decimal('10')),
            Ingrediente(nombre='Papas', unidad='kg', cantidad=Decimal('20')),
            Ingrediente(nombre='Carne para hamburguesa', unidad='unid', cantidad=Decimal('50')),
            Ingrediente(nombre='Queso', unidad='kg', cantidad=Decimal('10')),
            Ingrediente(nombre='Lechuga', unidad='unid', cantidad=Decimal('30')),
            Ingrediente(nombre='Cebolla', unidad='kg', cantidad=Decimal('10')),
            Ingrediente(nombre='Pollo', unidad='kg', cantidad=Decimal('15')),
            Ingrediente(nombre='Harina', unidad='kg', cantidad=Decimal('25')),
            Ingrediente(nombre='Huevo', unidad='unid', cantidad=Decimal('60')),
            Ingrediente(nombre='Bebida en lata', unidad='unid', cantidad=Decimal('100')),
            Ingrediente(nombre='Carne de vacuno', unidad='kg', cantidad=Decimal('20')),
            Ingrediente(nombre='Chorizo', unidad='unid', cantidad=Decimal('40')),
        ]
        session.add_all(ingredientes)
        session.commit()
        print("Ingredientes agregados.")

        # --- Menús ---
        # Helper para obtener un ingrediente por nombre
        def get_ing(nombre):
            return session.query(Ingrediente).filter_by(nombre=nombre).one()

        menus = [
            Menu(nombre='Completo', precio=Decimal('3500.00'), icono_path=os.path.join('IMG', 'completo.png')),
            Menu(nombre='Papas Fritas', precio=Decimal('2500.00'), icono_path=os.path.join('IMG', 'papas.png')),
            Menu(nombre='Hamburguesa', precio=Decimal('4500.00'), icono_path=os.path.join('IMG', 'hamburguesa.png')),
            Menu(nombre='Ensalada', precio=Decimal('3000.00'), icono_path=os.path.join('IMG', 'ensalada.png')),
            Menu(nombre='Pollo Asado', precio=Decimal('6000.00'), icono_path=os.path.join('IMG', 'pollo.png')),
            Menu(nombre='Panqueques', precio=Decimal('2000.00'), icono_path=os.path.join('IMG', 'panqueque.png')),
            Menu(nombre='Bebida', precio=Decimal('1500.00'), icono_path=os.path.join('IMG', 'bebida.png')),
            Menu(nombre='Chorrillana', precio=Decimal('8000.00'), icono_path=os.path.join('IMG', 'icono_chorrillana_64x64.png')),
        ]
        session.add_all(menus)
        session.commit()
        print("Menús agregados.")

        # --- Relaciones Menu-Ingrediente ---
        def get_menu(nombre):
            return session.query(Menu).filter_by(nombre=nombre).one()

        menu_ingredientes = [
            # Completo
            MenuIngrediente(menu=get_menu('Completo'), ingrediente=get_ing('Pan de completo'), cantidad_necesaria=Decimal('1')),
            MenuIngrediente(menu=get_menu('Completo'), ingrediente=get_ing('Vienesa'), cantidad_necesaria=Decimal('1')),
            MenuIngrediente(menu=get_menu('Completo'), ingrediente=get_ing('Tomate'), cantidad_necesaria=Decimal('0.1')),
            MenuIngrediente(menu=get_menu('Completo'), ingrediente=get_ing('Palta'), cantidad_necesaria=Decimal('0.1')),
            # Papas Fritas
            MenuIngrediente(menu=get_menu('Papas Fritas'), ingrediente=get_ing('Papas'), cantidad_necesaria=Decimal('0.5')),
            # Hamburguesa
            MenuIngrediente(menu=get_menu('Hamburguesa'), ingrediente=get_ing('Pan de completo'), cantidad_necesaria=Decimal('1')),
            MenuIngrediente(menu=get_menu('Hamburguesa'), ingrediente=get_ing('Carne para hamburguesa'), cantidad_necesaria=Decimal('1')),
            MenuIngrediente(menu=get_menu('Hamburguesa'), ingrediente=get_ing('Queso'), cantidad_necesaria=Decimal('0.05')),
            MenuIngrediente(menu=get_menu('Hamburguesa'), ingrediente=get_ing('Lechuga'), cantidad_necesaria=Decimal('0.1')),
            # Ensalada
            MenuIngrediente(menu=get_menu('Ensalada'), ingrediente=get_ing('Lechuga'), cantidad_necesaria=Decimal('0.5')),
            MenuIngrediente(menu=get_menu('Ensalada'), ingrediente=get_ing('Tomate'), cantidad_necesaria=Decimal('0.2')),
            # Pollo Asado
            MenuIngrediente(menu=get_menu('Pollo Asado'), ingrediente=get_ing('Pollo'), cantidad_necesaria=Decimal('0.5')),
            # Panqueques
            MenuIngrediente(menu=get_menu('Panqueques'), ingrediente=get_ing('Harina'), cantidad_necesaria=Decimal('0.2')),
            MenuIngrediente(menu=get_menu('Panqueques'), ingrediente=get_ing('Huevo'), cantidad_necesaria=Decimal('2')),
            # Bebida
            MenuIngrediente(menu=get_menu('Bebida'), ingrediente=get_ing('Bebida en lata'), cantidad_necesaria=Decimal('1')),
            # Chorrillana
            MenuIngrediente(menu=get_menu('Chorrillana'), ingrediente=get_ing('Papas'), cantidad_necesaria=Decimal('1')),
            MenuIngrediente(menu=get_menu('Chorrillana'), ingrediente=get_ing('Carne de vacuno'), cantidad_necesaria=Decimal('0.5')),
            MenuIngrediente(menu=get_menu('Chorrillana'), ingrediente=get_ing('Cebolla'), cantidad_necesaria=Decimal('0.3')),
            MenuIngrediente(menu=get_menu('Chorrillana'), ingrediente=get_ing('Chorizo'), cantidad_necesaria=Decimal('2')),
            MenuIngrediente(menu=get_menu('Chorrillana'), ingrediente=get_ing('Huevo'), cantidad_necesaria=Decimal('2')),
        ]
        session.add_all(menu_ingredientes)
        session.commit()
        print("Relaciones menu-ingrediente agregadas.")

        # --- Clientes ---
        clientes = [
            Cliente(nombre='Juan', apellido='Perez', email='juan.perez@example.com'),
            Cliente(nombre='Maria', apellido='Lopez', email='maria.lopez@example.com'),
            Cliente(nombre='Carlos', apellido='Gomez', email='carlos.gomez@example.com'),
            Cliente(nombre='Ana', apellido='Rodriguez', email='ana.rodriguez@example.com'),
            Cliente(nombre='Pedro', apellido='Sanchez', email='pedro.sanchez@example.com'),
        ]
        session.add_all(clientes)
        session.commit()
        print("Clientes agregados.")

        # --- Pedidos y PedidoItems ---
        all_clientes = session.query(Cliente).all()
        all_menus = session.query(Menu).all()
        estados = ['pendiente', 'completado', 'cancelado']
        tipos_entrega = ['local', 'domicilio']

        num_pedidos = 100 # Generar 100 pedidos para tener datos variados

        for i in range(num_pedidos):
            cliente = random.choice(all_clientes)
            fecha_pedido = datetime.now() - timedelta(days=random.randint(0, 60),
                                                      hours=random.randint(0, 23),
                                                      minutes=random.randint(0, 59))
            estado = random.choice(estados)
            tipo_entrega = random.choice(tipos_entrega)

            nuevo_pedido = Pedido(
                cliente_id=cliente.id,
                fecha=fecha_pedido,
                estado=estado,
                tipo_entrega=tipo_entrega,
                total=Decimal('0.00') # Se actualizará después de añadir items
            )
            session.add(nuevo_pedido)
            session.flush() # Para obtener el ID del pedido antes de añadir items

            total_pedido = Decimal('0.00')
            num_items = random.randint(1, 5) # Cada pedido tendrá entre 1 y 5 items

            for _ in range(num_items):
                menu_item = random.choice(all_menus)
                cantidad = randint(1, 3)
                precio_unitario = menu_item.precio
                subtotal = precio_unitario * cantidad
                total_pedido += subtotal

                pedido_item = PedidoItem(
                    pedido_id=nuevo_pedido.id,
                    menu_id=menu_item.id,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    subtotal=subtotal
                )
                session.add(pedido_item)

            nuevo_pedido.total = total_pedido
            session.add(nuevo_pedido) # Actualizar el total del pedido

        session.commit()
        print(f"{num_pedidos} pedidos y sus items agregados.")
        print("La base de datos ha sido poblada exitosamente.")

    except Exception as e:
        print(f"Ocurrió un error al poblar la base de datos: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    reset_database()
    populate_database()