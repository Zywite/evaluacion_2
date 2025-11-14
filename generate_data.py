import datetime
import random
from decimal import Decimal
from sqlalchemy.orm import Session
from database import get_db_session, initialize_database
from models import Cliente, Ingrediente, Menu, MenuIngrediente, Pedido, PedidoItem

def generate_sample_data(db: Session, num_clients=10, num_menus=10, num_pedidos=100):
    # Clear existing data (optional, for fresh generation)
    # db.query(PedidoItem).delete()
    # db.query(Pedido).delete()
    # db.query(MenuIngrediente).delete()
    # db.query(Menu).delete()
    # db.query(Ingrediente).delete()
    # db.query(Cliente).delete()
    # db.commit()

    print("Generando clientes...")
    clientes = []
    for i in range(num_clients):
        cliente = Cliente(
            nombre=f"Cliente{i}",
            apellido=f"Apellido{i}",
            email=f"cliente{i}@example.com"
        )
        db.add(cliente)
        clientes.append(cliente)
    db.commit()
    print(f"Generados {len(clientes)} clientes.")

    print("Generando ingredientes...")
    ingredientes_data = [
        ("Pan", "unidad", Decimal("100")), ("Carne", "gramos", Decimal("5000")),
        ("Lechuga", "hojas", Decimal("200")), ("Tomate", "unidades", Decimal("150")),
        ("Queso", "gramos", Decimal("3000")), ("Papas", "gramos", Decimal("10000")),
        ("Bebida", "ml", Decimal("5000")), ("Aderezo", "ml", Decimal("1000")),
        ("Cebolla", "unidades", Decimal("100")), ("Huevo", "unidades", Decimal("100")),
        ("Tocino", "gramos", Decimal("1000")), ("Palta", "unidades", Decimal("50")),
        ("Arroz", "gramos", Decimal("5000")), ("Pollo", "gramos", Decimal("5000")),
        ("Pescado", "gramos", Decimal("3000")), ("Camarones", "gramos", Decimal("1500")),
        ("Pasta", "gramos", Decimal("2000")), ("Salsa", "ml", Decimal("1000")),
        ("Champiñones", "gramos", Decimal("500")), ("Pimenton", "unidades", Decimal("50"))
    ]
    ingredientes = []
    for nombre, unidad, cantidad in ingredientes_data:
        ingrediente = Ingrediente(nombre=nombre, unidad=unidad, cantidad=cantidad)
        db.add(ingrediente)
        ingredientes.append(ingrediente)
    db.commit()
    print(f"Generados {len(ingredientes)} ingredientes.")

    print("Generando menús...")
    menus = []
    menu_definitions = [
        ("Hamburguesa Clásica", Decimal("8500"), ["Pan", "Carne", "Lechuga", "Tomate", "Queso"]),
        ("Papas Fritas", Decimal("3000"), ["Papas"]),
        ("Bebida Individual", Decimal("2000"), ["Bebida"]),
        ("Ensalada César", Decimal("7000"), ["Lechuga", "Pollo", "Aderezo"]),
        ("Sándwich de Pollo", Decimal("7500"), ["Pan", "Pollo", "Tomate", "Lechuga", "Mayonesa"]),
        ("Pizza Pepperoni", Decimal("12000"), ["Pan", "Queso", "Pepperoni", "Salsa"]),
        ("Pasta Alfredo", Decimal("9000"), ["Pasta", "Pollo", "Champiñones", "Salsa"]),
        ("Burrito de Carne", Decimal("9500"), ["Carne", "Arroz", "Frijoles", "Queso", "Lechuga"]),
        ("Tacos de Pescado", Decimal("8000"), ["Pescado", "Tortilla", "Col", "Salsa"]),
        ("Jugo Natural", Decimal("3500"), ["Fruta", "Agua"])
    ]

    for name, price, ingredient_names in menu_definitions:
        menu = Menu(nombre=name, precio=price, icono_path=f"IMG/{name.lower().replace(' ', '_')}.png")
        db.add(menu)
        db.flush() # Flush to get menu.id

        for ing_name in ingredient_names:
            ing = next((i for i in ingredientes if i.nombre == ing_name), None)
            if ing:
                menu_ingrediente = MenuIngrediente(
                    menu_id=menu.id,
                    ingrediente_id=ing.id,
                    cantidad_necesaria=Decimal(random.uniform(0.1, 2.0)) # Random quantity
                )
                db.add(menu_ingrediente)
        menus.append(menu)
    db.commit()
    print(f"Generados {len(menus)} menús.")

    print("Generando pedidos y sus ítems...")
    start_date = datetime.datetime.now() - datetime.timedelta(days=365) # Data for the last year
    for i in range(num_pedidos):
        cliente = random.choice(clientes)
        
        # Random date within the last year
        random_days = random.randint(0, 365)
        random_seconds = random.randint(0, 24*60*60 - 1)
        fecha_pedido = start_date + datetime.timedelta(days=random_days, seconds=random_seconds)

        pedido = Pedido(
            cliente_id=cliente.id,
            fecha=fecha_pedido,
            total=Decimal("0.00") # Will be updated after adding items
        )
        db.add(pedido)
        db.flush() # Flush to get pedido.id

        num_items = random.randint(1, 5)
        pedido_total = Decimal("0.00")
        for _ in range(num_items):
            menu = random.choice(menus)
            cantidad = random.randint(1, 3)
            precio_unitario = menu.precio
            
            pedido_item = PedidoItem(
                pedido_id=pedido.id,
                menu_id=menu.id,
                cantidad=cantidad,
                precio_unitario=precio_unitario
            )
            db.add(pedido_item)
            pedido_total += precio_unitario * cantidad
        
        pedido.total = pedido_total
        db.add(pedido) # Re-add to update the total
    db.commit()
    print(f"Generados {num_pedidos} pedidos con sus ítems.")

    print("Generación de datos completada.")

if __name__ == "__main__":
    # Ensure tables are created before generating data
    initialize_database()
    
    db_session = get_db_session()
    try:
        generate_sample_data(db_session, num_clients=20, num_menus=15, num_pedidos=500)
    except Exception as e:
        db_session.rollback()
        print(f"Error durante la generación de datos: {e}")
    finally:
        db_session.close()
