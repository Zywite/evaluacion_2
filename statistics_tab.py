import customtkinter as ctk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from CTkMessagebox import CTkMessagebox
from database import get_db_session
from models import Pedido, Menu, Ingrediente, PedidoItem, MenuIngrediente
from sqlalchemy import func, extract, cast, Date
from datetime import datetime, timedelta

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

        ctk.CTkLabel(control_frame, text="Tipo de Gráfico:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
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
        self.chart_type_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Date range selection for "Ventas por Fecha"
        self.date_range_label = ctk.CTkLabel(control_frame, text="Rango de Ventas:")
        self.date_range_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.date_range_combobox = ctk.CTkComboBox(
            control_frame,
            values=["Diarias", "Semanales", "Mensuales", "Anuales"],
            command=self.on_date_range_selected
        )
        self.date_range_combobox.set("Diarias")
        self.date_range_combobox.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        self.generate_button = ctk.CTkButton(control_frame, text="Generar Gráfico", command=self.generate_chart)
        self.generate_button.grid(row=0, column=4, padx=5, pady=5, sticky="e")

        self.generate_chart() # Generate initial chart on load

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
            date_range = self.date_range_combobox.get()
            
            if date_range == "Diarias":
                sales_data = session.query(
                    cast(Pedido.fecha, Date),
                    func.sum(Pedido.total)
                ).group_by(cast(Pedido.fecha, Date)).order_by(cast(Pedido.fecha, Date)).all()
            elif date_range == "Semanales":
                sales_data = session.query(
                    func.to_char(Pedido.fecha, 'YYYY-WW'), # Week number of the year
                    func.sum(Pedido.total)
                ).group_by(func.to_char(Pedido.fecha, 'YYYY-WW')).order_by(func.to_char(Pedido.fecha, 'YYYY-WW')).all()
            elif date_range == "Mensuales":
                sales_data = session.query(
                    func.to_char(Pedido.fecha, 'YYYY-MM'),
                    func.sum(Pedido.total)
                ).group_by(func.to_char(Pedido.fecha, 'YYYY-MM')).order_by(func.to_char(Pedido.fecha, 'YYYY-MM')).all()
            elif date_range == "Anuales":
                sales_data = session.query(
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
            ax.set_title(f'Ventas {date_range}')
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
            top_menus_data = (session.query(
                Menu.nombre,
                func.sum(PedidoItem.cantidad).label('total_vendido')
            ).join(PedidoItem, Menu.id == PedidoItem.menu_id)
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
            ax.set_title('Distribución de Menús más Comprados')
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
            ingredient_usage_data = (session.query(
                Ingrediente.nombre,
                func.sum(PedidoItem.cantidad * MenuIngrediente.cantidad_necesaria).label('total_cantidad_usada')
            ).join(MenuIngrediente, Ingrediente.id == MenuIngrediente.ingrediente_id)
            .join(Menu, Menu.id == MenuIngrediente.menu_id)
            .join(PedidoItem, Menu.id == PedidoItem.menu_id)
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
            ax.set_title('Uso de Ingredientes en Pedidos (por cantidad)')
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