# menu_catalog.py
from typing import List
from ElementoMenu import CrearMenu
from Ingrediente import Ingrediente
from IMenu import IMenu

def get_default_menus() -> List[IMenu]:
    return [
        CrearMenu(
            "Papas Fritas",
            [
                Ingrediente("Papas", "unid", 2.0),
            ],
            precio=500,
            icono_path="IMG/papas.png",
        ),
        CrearMenu(
            "Pepsi",
            [
                Ingrediente("Pepsi", "unid", 1.0),
            ],
            precio=1100,
            icono_path="IMG/bebida.png",
        ),
        CrearMenu(
            "Completo",
            [
                Ingrediente("Vienesa", "unid", 1.0),
                Ingrediente("Pan de completo", "unid", 1.0),
                Ingrediente("Tomate", "unid", 1.0),
                Ingrediente("Palta", "unid", 1.0),
            ],
            precio=1800,
            icono_path="IMG/completo.png",
        ),
        CrearMenu(
            "Hamburguesa",
            [
                Ingrediente("Pan de hamburguesa", "unid", 1.0),
                Ingrediente("Lamina de queso", "unid", 1.0),
                Ingrediente("Churrasco de carne", "unid", 1.0),
            ],
            precio=3500,
            icono_path="IMG/hamburguesa.png",
        ),
        CrearMenu(
            "Panqueques",
            [
                Ingrediente("Panqueques", "unid", 2.0),
                Ingrediente("Manjar", "unid", 1.0),
                Ingrediente("Azúcar flor", "unid", 1.0),
            ],
            precio=2000,
            icono_path="IMG/panqueque.png",
        ),
        CrearMenu(
            "Pollo Frito",
            [
                Ingrediente("Presa de pollo", "unid", 1.0),
                Ingrediente("Harina", "unid", 2.0),
                Ingrediente("Aceite", "unid", 1.0),
            ],
            precio=2800,
            icono_path="IMG/pollo.png",
        ),
        CrearMenu(
            "Ensalada Mixta",
            [
                Ingrediente("Lechuga", "unid", 1.0),
                Ingrediente("Tomate", "unid", 1.0),
                Ingrediente("Zanahoria", "unid", 1.0),
            ],
            precio=1500,
            icono_path="IMG/ensalada.png",
        ),
    ]