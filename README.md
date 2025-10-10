# Sistema de Gestión de Restaurante

Sistema de gestión para restaurantes implementado en Python con interfaz gráfica usando customtkinter.

## Características

- Gestión de inventario de ingredientes
- Sistema de pedidos
- Generación de boletas
- Visualización de menú en PDF
- Interfaz gráfica moderna

## Requisitos

- Python 3.x
- customtkinter
- Pillow (PIL)
- PyMuPDF
- pandas

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/ev2_progra2.git
cd ev2_progra2
```

2. Crear un entorno virtual:
```bash
python -m venv .venv
```

3. Activar el entorno virtual:
- Windows:
```bash
.venv\Scripts\activate
```
- Linux/Mac:
```bash
source .venv/bin/activate
```

4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

Para ejecutar el programa:
```bash
python Restaurante.py
```

## Estructura del Proyecto

- `Restaurante.py`: Aplicación principal y GUI
- `BoletaFacade.py`: Generación de boletas
- `ElementoMenu.py`: Definición de elementos del menú
- `Ingrediente.py`: Clase para ingredientes
- `Menu_catalog.py`: Catálogo de menús
- `Pedido.py`: Gestión de pedidos
- `Stock.py`: Control de inventario
- `menu_pdf.py`: Generación de PDFs

## Autores

- Joaquin Carrasco Duran
- Benjamin Cabrera

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.