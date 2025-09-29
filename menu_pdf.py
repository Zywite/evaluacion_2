# menu_pdf.py
from fpdf import FPDF
from typing import List
from IMenu import IMenu
import os

def _latin1(s: str) -> str:
    return s.encode("latin-1", "replace").decode("latin-1")

def create_menu_pdf(
    menus: List[IMenu],
    pdf_path: str = "carta.pdf",
    titulo_negocio: str = "Carta del Restaurante",
    subtitulo: str = "Menú del día",
    moneda: str = "$",
    # Colores (RGB)
    color_primario=(33, 150, 243),   # azul
    color_header_text=(255, 255, 255),
    color_fila_par=(245, 247, 250),  # gris muy claro
    color_fila_impar=(255, 255, 255) # blanco
) -> str:
    """
    Genera un PDF de la carta solo con Nombre y Precio, con estilo:
    - Banner de título con color
    - Encabezado de tabla coloreado
    - Filas 'zebra'
    - Precios alineados a la derecha
    """
    # Layout
    margen = 12
    col_w_nombre = 120
    col_w_precio = 50
    row_h = 10

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=margen)
    pdf.add_page()

    # ---------- Banner superior ----------
    pdf.set_fill_color(*color_primario)
    pdf.rect(0, 0, 210, 30, style="F")  # ancho A4
    pdf.set_xy(margen, 8)
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(*color_header_text)
    pdf.cell(0, 10, _latin1(titulo_negocio), ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.set_x(margen)
    pdf.cell(0, 8, _latin1(subtitulo), ln=True)

    # espacio bajo banner
    pdf.ln(6)

    # ---------- Encabezado de tabla ----------
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(230, 236, 241)         # gris suave header
    pdf.set_text_color(0, 0, 0)
    pdf.cell(col_w_nombre, row_h, _latin1("Menú"), border=0, ln=0, align="L", fill=True)
    pdf.cell(col_w_precio, row_h, _latin1("Precio"), border=0, ln=1, align="R", fill=True)

    # Línea separadora
    pdf.set_draw_color(220, 220, 220)
    x1 = margen
    x2 = margen + col_w_nombre + col_w_precio
    y = pdf.get_y()
    pdf.line(x1, y, x2, y)

    # ---------- Filas ----------
    pdf.set_font("Arial", "", 12)
    for i, menu in enumerate(menus):
        # Zebra
        is_par = (i % 2 == 0)
        bg = color_fila_par if is_par else color_fila_impar
        pdf.set_fill_color(*bg)

        nombre = _latin1(menu.nombre)
        precio = f"{moneda}{menu.precio:,.0f}".replace(",", ".")

        # Nombre
        pdf.cell(col_w_nombre, row_h, nombre, border=0, ln=0, align="L", fill=True)
        # Precio (alineado a la derecha)
        pdf.cell(col_w_precio, row_h, _latin1(precio), border=0, ln=1, align="R", fill=True)

    # ---------- Footer sutil ----------
    pdf.set_y(-18)
    pdf.set_font("Arial", "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 8, _latin1("Gracias por su preferencia."), align="C")

    abs_path = os.path.abspath(pdf_path)
    pdf.output(abs_path)
    return abs_path
