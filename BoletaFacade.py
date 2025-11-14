from fpdf import FPDF
from datetime import datetime
import os
from database import get_db_session
from models import Pedido as PedidoModel, PedidoItem
from sqlalchemy.orm import Session, joinedload

class BoletaFacade:
    """
    Implementa el patrón de diseño Facade (Fachada).

    Esta clase simplifica la compleja tarea de generar una boleta. Oculta toda la lógica
    de cálculo de totales, IVA y formato del PDF detrás de un método simple y único: `generar_boleta()`.
    El cliente (en este caso, la clase Restaurante) solo necesita interactuar con esta fachada,
    sin preocuparse por los detalles internos de la creación del PDF.
    """
    def __init__(self, pedido_id):
        self.pedido_id = pedido_id
        self.detalle_items = []
        self.subtotal = 0
        self.iva = 0
        self.total = 0
        self.fecha_pedido = datetime.now()  # Inicializar con la fecha y hora actual
        self.cliente_nombre = ""
        self.cliente_email = ""

    def generar_detalle_boleta(self):
        session: Session = get_db_session()
        try:
            pedido_db = session.query(PedidoModel).options(
                joinedload(PedidoModel.items).joinedload(PedidoItem.menu),
                joinedload(PedidoModel.cliente)
            ).filter(PedidoModel.id == self.pedido_id).one_or_none()

            print(f"DEBUG: Buscando pedido con ID: {self.pedido_id}") # Debug print
            if pedido_db:
                print(f"DEBUG: Pedido con ID {self.pedido_id} encontrado.") # Debug print
                self.fecha_pedido = pedido_db.fecha
                self.total = float(pedido_db.total)
                self.subtotal = round(self.total / 1.19, 2)
                self.iva = round(self.total - self.subtotal, 2)

                # Obtener información del cliente
                if pedido_db.cliente:
                    self.cliente_nombre = f"{pedido_db.cliente.nombre} {pedido_db.cliente.apellido}"
                    self.cliente_email = pedido_db.cliente.email

                for item in pedido_db.items:
                    self.detalle_items.append({
                        'nombre': item.menu.nombre,
                        'cantidad': item.cantidad,
                        'precio_unitario': float(item.precio_unitario)
                    })
                return True  # Indicar que los detalles se cargaron correctamente
            print(f"DEBUG: Pedido con ID {self.pedido_id} NO encontrado.") # Debug print
            return False  # Indicar que no se encontró el pedido
        finally:
            session.close()

    def crear_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Boleta Restaurante", ln=True, align='L')
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, "Razón Social del Negocio", ln=True, align='L')
        pdf.cell(0, 10, "RUT: 12345678-9", ln=True, align='L')
        pdf.cell(0, 10, "Dirección: Calle Falsa 123", ln=True, align='L')
        pdf.cell(0, 10, "Teléfono: +56 9 1234 5678", ln=True, align='L')
        pdf.ln(5)
        
        # Información del cliente
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Datos del Cliente", ln=True, align='L')
        pdf.set_font("Arial", size=11)
        pdf.cell(0, 8, f"Cliente: {self.cliente_nombre}", ln=True, align='L')
        pdf.cell(0, 8, f"Email: {self.cliente_email}", ln=True, align='L')
        pdf.cell(0, 8, f"Fecha: {self.fecha_pedido.strftime('%d/%m/%Y %H:%M:%S')}", ln=True, align='L')
        pdf.ln(10)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(70, 10, "Nombre", border=1)
        pdf.cell(20, 10, "Cantidad", border=1)
        pdf.cell(35, 10, "Precio Unitario", border=1)
        pdf.cell(30, 10, "Subtotal", border=1)
        pdf.ln()
        
        pdf.set_font("Arial", size=12)
        for item in self.detalle_items:
            nombre = item['nombre']
            cantidad = item['cantidad']
            precio_unitario = item['precio_unitario']
            subtotal_item = precio_unitario * cantidad
            pdf.cell(70, 10, nombre, border=1)
            pdf.cell(20, 10, str(cantidad), border=1)
            pdf.cell(35, 10, f"${precio_unitario:.2f}", border=1)
            pdf.cell(30, 10, f"${subtotal_item:.2f}", border=1)
            pdf.ln()

        pdf.set_font("Arial", 'B', 12)
        pdf.cell(120, 10, "Subtotal:", 0, 0, 'R')
        pdf.cell(30, 10, f"${self.subtotal:.2f}", ln=True, align='R')
        
        pdf.cell(120, 10, "IVA (19%):", 0, 0, 'R')
        pdf.cell(30, 10, f"${self.iva:.2f}", ln=True, align='R')
        
        pdf.cell(120, 10, "Total:", 0, 0, 'R')
        pdf.cell(30, 10, f"${self.total:.2f}", ln=True, align='R')
        
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(0, 10, "Gracias por su compra. Para cualquier consulta, llámenos al +56 9 777 5678.", 0, 1, 'C')
        pdf.cell(0, 10, "Los productos adquiridos no tienen garantía.", 0, 1, 'C')
        

        # Crear un nombre único para la boleta usando timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"boleta_{timestamp}.pdf"
        
        # Crear directorio para boletas si no existe
        boletas_dir = "boletas"
        if not os.path.exists(boletas_dir):
            os.makedirs(boletas_dir)
            
        # Guardar en el directorio de boletas
        pdf_path = os.path.join(boletas_dir, pdf_filename)
        pdf.output(pdf_path)
        return pdf_path

    def generar_boleta(self):
        """Coordina la generación de la boleta y la creación del PDF."""
        if self.generar_detalle_boleta():
            return self.crear_pdf()
        else:
            # Manejar el caso en que el pedido no se encuentra
            raise Exception(f"No se pudo generar la boleta porque el pedido con ID {self.pedido_id} no fue encontrado.")