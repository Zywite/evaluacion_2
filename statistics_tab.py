import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from CTkMessagebox import CTkMessagebox
from database import get_db_session
from models import Pedido, Menu, Ingrediente, PedidoItem, MenuIngrediente
from sqlalchemy import func, extract, cast, Date

class StatisticsTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.chart_frame = ctk.CTkFrame(self)
        self.chart_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.chart_frame.grid_columnconfigure(0, weight=1)
        self.chart_frame.grid_rowconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # Top frame for controls
        control_frame = ctk.CTkFrame(self)
        control_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        control_frame.grid_columnconfigure(0, weight=1)
        control_frame.grid_columnconfigure(1, weight=1)
        control_frame.grid_columnconfigure(2, weight=1)
        control_frame.grid_columnconfigure(3, weight=1)
        control_frame.grid_columnconfigure(4, weight=1)
        control_frame.grid_columnconfigure(5, weight=1)

        # Cliente selector
        ctk.CTkLabel(control_frame, text="Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.clientes_disponibles = self._obtener_clientes()
        opciones_clientes = ["Todos"] + self.clientes_disponibles
        self.cliente_combobox = ctk.CTkComboBox(
            control_frame,
            values=opciones_clientes,
            command=self.on_cliente_selected
        )
        self.cliente_combobox.set("Todos")
        self.cliente_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Chart type selector
        ctk.CTkLabel(control_frame, text="Tipo de Gráfico:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.chart_type_combobox = ctk.CTkComboBox(
            control_frame,
            values=[
                "Ventas por Fecha",
                "Distribución de Menús más Comprados",
                "Uso de Ingredientes en Pedidos"
            ],
            command=self.on_chart_type_selected
        )
        self.chart_type_combobox.set("Ventas por Fecha")
        self.chart_type_combobox.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Date range selection for "Ventas por Fecha"
        self.date_range_label = ctk.CTkLabel(control_frame, text="Rango de Ventas:")
        self.date_range_label.grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.date_range_combobox = ctk.CTkComboBox(
            control_frame,
            values=["Diarias", "Semanales", "Mensuales", "Anuales"],
            command=self.on_date_range_selected
        )
        self.date_range_combobox.set("Diarias")
        self.date_range_combobox.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

        self.generate_button = ctk.CTkButton(control_frame, text="Generar Gráfico", command=self.generate_chart)
        self.generate_button.grid(row=0, column=6, padx=5, pady=5, sticky="e")

        self.generate_chart() # Generate initial chart on load

    def _obtener_clientes(self):
        """Obtiene lista de clientes de la base de datos"""
        session = get_db_session()
        try:
            from models import Cliente
            clientes = session.query(Cliente).all()
            return [f"{cliente.nombre} {cliente.apellido}" for cliente in clientes]
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error al cargar clientes: {e}")
            return []
        finally:
            session.close()

    def on_cliente_selected(self, cliente_nombre):
        """Manejador cuando cambia el cliente seleccionado"""
        self.generate_chart()

    def on_chart_type_selected(self, choice):
        if choice == "Ventas por Fecha":
            self.date_range_label.grid()
            self.date_range_combobox.grid()
        else:
            self.date_range_label.grid_remove()
            self.date_range_combobox.grid_remove()
        self.generate_chart()

    def on_date_range_selected(self, choice):
        self.generate_chart()

    def clear_chart_frame(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

    def show_no_data_message(self, message="No hay datos disponibles para graficar."):
        self.clear_chart_frame()
        no_data_label = ctk.CTkLabel(self.chart_frame, text=message, font=("Helvetica", 15, "bold"))
        no_data_label.place(relx=0.5, rely=0.5, anchor="center")

    def generate_chart(self):
        self.clear_chart_frame()
        chart_type = self.chart_type_combobox.get()

        if chart_type == "Ventas por Fecha":
            self.generate_sales_by_date_chart()
        elif chart_type == "Distribución de Menús más Comprados":
            self.generate_top_menus_chart()
        elif chart_type == "Uso de Ingredientes en Pedidos":
            self.generate_ingredient_usage_chart()

    def generate_sales_by_date_chart(self):
        session = get_db_session()
        try:
            from models import Cliente
            date_range = self.date_range_combobox.get()
            cliente_seleccionado = self.cliente_combobox.get()
            
            # Base query con filtro de cliente si es necesario
            query = session.query(Pedido)
            if cliente_seleccionado != "Todos":
                nombre_apellido = cliente_seleccionado.split()
                nombre = nombre_apellido[0]
                apellido = " ".join(nombre_apellido[1:]) if len(nombre_apellido) > 1 else ""
                query = query.join(Cliente).filter(
                    (Cliente.nombre == nombre) & (Cliente.apellido == apellido)
                )
            
            if date_range == "Diarias":
                sales_data = query.with_entities(
                    cast(Pedido.fecha, Date),
                    func.sum(Pedido.total)
                ).group_by(cast(Pedido.fecha, Date)).order_by(cast(Pedido.fecha, Date)).all()
            elif date_range == "Semanales":
                sales_data = query.with_entities(
                    func.to_char(Pedido.fecha, 'YYYY-WW'),
                    func.sum(Pedido.total)
                ).group_by(func.to_char(Pedido.fecha, 'YYYY-WW')).order_by(func.to_char(Pedido.fecha, 'YYYY-WW')).all()
            elif date_range == "Mensuales":
                sales_data = query.with_entities(
                    func.to_char(Pedido.fecha, 'YYYY-MM'),
                    func.sum(Pedido.total)
                ).group_by(func.to_char(Pedido.fecha, 'YYYY-MM')).order_by(func.to_char(Pedido.fecha, 'YYYY-MM')).all()
            elif date_range == "Anuales":
                sales_data = query.with_entities(
                    extract('year', Pedido.fecha),
                    func.sum(Pedido.total)
                ).group_by(extract('year', Pedido.fecha)).order_by(extract('year', Pedido.fecha)).all()
            else:
                self.show_no_data_message("Tipo de rango de fecha no soportado.")
                return

            if not sales_data:
                self.show_no_data_message("No hay datos de ventas disponibles para el rango seleccionado.")
                return

            dates = [str(row[0]) for row in sales_data]
            totals = [float(row[1]) for row in sales_data]

            fig, ax = plt.subplots(figsize=(9, 6))
            ax.plot(dates, totals, marker='o', linestyle='-')
            titulo = f'Ventas {date_range}'
            if cliente_seleccionado != "Todos":
                titulo += f" - {cliente_seleccionado}"
            ax.set_title(titulo)
            ax.set_xlabel('Fecha')
            ax.set_ylabel('Total de Ventas ($)')
            plt.xticks(rotation=44, ha='right')
            plt.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)
            canvas.draw()

        except Exception as e:
            CTkMessagebox(title="Error de Gráfico", message=f"Error al generar el gráfico de ventas: {e}")
            self.show_no_data_message("Error al cargar los datos de ventas.")
        finally:
            session.close()

    def generate_top_menus_chart(self):
        session = get_db_session()
        try:
            from models import Cliente
            cliente_seleccionado = self.cliente_combobox.get()
            
            # Base query
            query = (session.query(
                Menu.nombre,
                func.sum(PedidoItem.cantidad).label('total_vendido')
            ).join(PedidoItem, Menu.id == PedidoItem.menu_id)
            .join(Pedido, PedidoItem.pedido_id == Pedido.id))
            
            # Filtrar por cliente si es necesario
            if cliente_seleccionado != "Todos":
                nombre_apellido = cliente_seleccionado.split()
                nombre = nombre_apellido[0]
                apellido = " ".join(nombre_apellido[1:]) if len(nombre_apellido) > 1 else ""
                query = query.join(Cliente, Pedido.cliente_id == Cliente.id).filter(
                    (Cliente.nombre == nombre) & (Cliente.apellido == apellido)
                )
            
            top_menus_data = (query
            .group_by(Menu.nombre)
            .order_by(func.sum(PedidoItem.cantidad).desc())
            .limit(9)).all()

            if not top_menus_data:
                self.show_no_data_message("No hay datos de menús vendidos disponibles.")
                return

            menu_names = [row[0] for row in top_menus_data]
            quantities = [row[1] for row in top_menus_data]

            fig, ax = plt.subplots(figsize=(9, 6))
            ax.bar(menu_names, quantities, color='skyblue')
            titulo = 'Distribución de Menús más Comprados'
            if cliente_seleccionado != "Todos":
                titulo += f" - {cliente_seleccionado}"
            ax.set_title(titulo)
            ax.set_xlabel('Menú')
            ax.set_ylabel('Cantidad Vendida')
            plt.xticks(rotation=44, ha='right')
            plt.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)
            canvas.draw()

        except Exception as e:
            CTkMessagebox(title="Error de Gráfico", message=f"Error al generar el gráfico de menús: {e}")
            self.show_no_data_message("Error al cargar los datos de menús.")
        finally:
            session.close()

    def generate_ingredient_usage_chart(self):
        session = get_db_session()
        try:
            from models import Cliente
            cliente_seleccionado = self.cliente_combobox.get()
            
            # Base query
            query = (session.query(
                Ingrediente.nombre,
                func.sum(PedidoItem.cantidad * MenuIngrediente.cantidad_necesaria).label('total_cantidad_usada')
            ).join(MenuIngrediente, Ingrediente.id == MenuIngrediente.ingrediente_id)
            .join(Menu, Menu.id == MenuIngrediente.menu_id)
            .join(PedidoItem, Menu.id == PedidoItem.menu_id)
            .join(Pedido, PedidoItem.pedido_id == Pedido.id))
            
            # Filtrar por cliente si es necesario
            if cliente_seleccionado != "Todos":
                nombre_apellido = cliente_seleccionado.split()
                nombre = nombre_apellido[0]
                apellido = " ".join(nombre_apellido[1:]) if len(nombre_apellido) > 1 else ""
                query = query.join(Cliente, Pedido.cliente_id == Cliente.id).filter(
                    (Cliente.nombre == nombre) & (Cliente.apellido == apellido)
                )
            
            ingredient_usage_data = (query
            .group_by(Ingrediente.nombre)
            .order_by(func.sum(PedidoItem.cantidad * MenuIngrediente.cantidad_necesaria).desc())
            .limit(9)).all()

            if not ingredient_usage_data:
                self.show_no_data_message("No hay datos de uso de ingredientes disponibles.")
                return

            ingredient_names = [row[0] for row in ingredient_usage_data]
            usage_quantities = [float(row[1]) for row in ingredient_usage_data]

            fig, ax = plt.subplots(figsize=(9, 6))
            ax.pie(usage_quantities, labels=ingredient_names, autopct='%0.1f%%', startangle=90)
            titulo = 'Uso de Ingredientes en Pedidos (por cantidad)'
            if cliente_seleccionado != "Todos":
                titulo += f" - {cliente_seleccionado}"
            ax.set_title(titulo)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            plt.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)
            canvas.draw()

        except Exception as e:
            CTkMessagebox(title="Error de Gráfico", message=f"Error al generar el gráfico de ingredientes: {e}")
            self.show_no_data_message("Error al cargar los datos de ingredientes.")
        finally:
            session.close()