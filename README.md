# Sistema de Gestión de Restaurante

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Sistema de gestión para restaurantes implementado en Python con una moderna interfaz gráfica construida con el framework `customtkinter`.

## Características

- Gestión de inventario de ingredientes
- Sistema de pedidos y toma de órdenes en tiempo real.
- Generación de boletas en formato PDF.
- Visualizador de documentos PDF integrado para la carta y las boletas.
- Carga de ingredientes desde archivos CSV.
- Interfaz gráfica moderna y personalizable.

## Requisitos

- Python 3.10 o superior.
- Todas las dependencias están listadas en el archivo `requirements.txt`.

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/Zywite/evaluacion_2.git
cd evaluacion_2
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
- Leonardo Chavez

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
