from decimal import Decimal, InvalidOperation
import customtkinter as ctk
from tkinter import ttk
from tkinter import filedialog
from tkinter.font import nametofont
from Ingrediente import Ingrediente
from Stock import Stock
import re
from PIL import Image
from CTkMessagebox import CTkMessagebox #para los mensajes
from Pedido import Pedido
from BoletaFacade import BoletaFacade
import pandas as pd #pandas
from menu_pdf import create_menu_pdf
from ctk_pdf_viewer import CTkPDFViewer #para ver los pdf
import os # para manejar las rutas
from database import initialize_database, get_db_session
from models import Cliente
from sqlalchemy.exc import IntegrityError
from crud import cliente_crud, pedido_crud, ingrediente_crud, menu_crud
from ElementoMenu import CrearMenu
from statistics_tab import StatisticsTab
from error_handler import (
    logger,                  # Logger centralizado
    ValidadorCantidad,       # Validador de cantidades (Template Method)
    ValidadorNombre,         # Validador de nombres (Template Method)
)
from reportes import generar_reporte  # Generador de reportes (JSON, CSV, HTML)
import subprocess  # Para abrir archivos
#importamos todo lo que sea necesario

class AplicacionConPestanas(ctk.CTk): # se crea la clase de la aplicacion para las ventanas
    def __init__(self):
        initialize_database() # Initialize the database
        super().__init__() # se inicia la clase padre
        
        self.title("Gestión de Restaurante") 
        self.geometry("950x700")
        nametofont("TkHeadingFont").configure(size=14) 
        nametofont("TkDefaultFont").configure(size=11) #tamaño de letra
        #configuracion de la ventana

        # Configuración de estilos de botones
        self.button_styles = {
            'primary': {
                'fg_color': "#2196F3",  # Azul material
                'hover_color': "#1976D2",  # Azul más oscuro
                'text_color': "white", #texto color blanco
                'corner_radius': 8, # borde redondeado
                'border_width': 0, # sin borde
                'font': ('Helvetica', 12, 'bold')
                #tamaño de fuente en negrita
            },
            'secondary': { #estilo secundario
                'fg_color': "#4CAF50",  # Verde material
                'hover_color': "#388E3C",  # Verde más oscuro
                'text_color': "white", #texto color blanco (cambio de negro a blanco para mejor contraste)
                'corner_radius': 8, # borde redondeado
                'border_width': 0, # sin borde
                'font': ('Helvetica', 12, 'bold') #tamaño de fuente en negrita
            },
            'danger': { #estilo de peligro
                'fg_color': "#F44336",  # Rojo material
                'hover_color': "#D32F2F",  # Rojo más oscuro
                'text_color': "white", #texto color blanco
                'corner_radius': 8, # borde redondeado
                'border_width': 0, # sin borde
                'font': ('Helvetica', 12, 'bold') #tamaño de fuente en negrita
            }
        }

        self.stock = Stock() # se crea el stock
        self.menus_creados = set() #se crea un conjunto vacio para los menus creados
        self.pedido = Pedido() # se crea el pedido
        self.clientes = {} # Diccionario para almacenar clientes cargados

        self.menus = []
  
        self.tabview = ctk.CTkTabview(self,command=self.on_tab_change) # se crea la pestaña
        self.tabview.pack(expand=True, fill="both", padx=10, pady=10) # se empaqueta la pestaña

        self.crear_pestanas() # se crean las pestañas
        
        # Configurar el manejador de cierre para evitar errores al cerrar
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def actualizar_treeview(self): # se crea para actualizar el treeview
        for item in self.tree.get_children(): # se recorre el treeview con un for
            self.tree.delete(item) # se elimina el item

        # Iterar sobre los valores del diccionario de stock
        for ingrediente in self.stock.lista_ingredientes.values(): # se recorre los ingredientes del stock
            self.tree.insert("", "end", values=(ingrediente.nombre, ingrediente.unidad, ingrediente.cantidad))    
            #se inserta el ingrediente en el treeview
        
        # Actualizar la visualización de los menús cuando cambia el stock
        self.actualizar_menus()

    def on_tab_change(self): #se crea la funcion de cambio de pantalla
        selected_tab = self.tabview.get() # se obtiene la pestaña seleccionada
        if selected_tab == "Gestión de Clientes":
            self.cargar_clientes_en_treeview()
        elif selected_tab == "Pedido":
            self.actualizar_clientes_combobox()
        elif selected_tab in ["Carga de ingredientes", "Stock", "Carta restorante", "Boleta"]: # si la pestaña es una de estas
            self.actualizar_treeview() # se actualiza la pantalla
    
    def on_closing(self):
        """Manejador de cierre de la aplicación para evitar errores de callbacks pendientes"""
        try:
            # Cancelar todos los callbacks pendientes
            try:
                for after_id in list(self.tk.call('after', 'info')):
                    try:
                        self.after_cancel(after_id)
                    except Exception:
                        pass
            except Exception:
                pass
            
            # Detener el event loop primero
            self.quit()
        except Exception:
            pass
        finally:
            # Destruir la ventana
            try:
                self.destroy()
            except Exception:
                pass
    
    def crear_pestanas(self): # se crea la funcion de crear las pestañas
        self.tab_clientes = self.tabview.add("Gestión de Clientes")
        self.tab3 = self.tabview.add("Carga de ingredientes")  
        self.tab1 = self.tabview.add("Stock")
        self.tab4 = self.tabview.add("Carta restorante")  
        self.tab2 = self.tabview.add("Pedido")
        self.tab5 = self.tabview.add("Boleta")
        self.tab_estadisticas = self.tabview.add("Estadísticas")
        self.tab_reportes = self.tabview.add("Reportes")
        # se crean las diferente pestañas con todos sus nombres
        self.configurar_pestana_clientes()
        self.configurar_pestana1()
        self.configurar_pestana2()
        self.configurar_pestana3()
        self._configurar_pestana_crear_menu()
        self._configurar_pestana_ver_boleta()
        self._configurar_pestana_estadisticas()
        self._configurar_pestana_reportes()
        # se configuran las pestañas con sus funciones

    def configurar_pestana_clientes(self):
        # --- Layout ---
        frame_principal = ctk.CTkFrame(self.tab_clientes)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)
        frame_principal.grid_columnconfigure(1, weight=1)
        frame_principal.grid_rowconfigure(0, weight=1)

        frame_formulario = ctk.CTkFrame(frame_principal)
        frame_formulario.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        frame_treeview = ctk.CTkFrame(frame_principal)
        frame_treeview.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        frame_treeview.grid_rowconfigure(0, weight=1)
        frame_treeview.grid_columnconfigure(0, weight=1)

        # --- Formulario ---
        ctk.CTkLabel(frame_formulario, text="Gestión de Clientes").pack(pady=10, anchor="center")

        ctk.CTkLabel(frame_formulario, text="Nombre:").pack(pady=(10,0), padx=10, anchor="w")
        self.entry_cliente_nombre = ctk.CTkEntry(frame_formulario)
        self.entry_cliente_nombre.pack(pady=5, padx=10, fill="x")

        ctk.CTkLabel(frame_formulario, text="Apellido:").pack(pady=(10,0), padx=10, anchor="w")
        self.entry_cliente_apellido = ctk.CTkEntry(frame_formulario)
        self.entry_cliente_apellido.pack(pady=5, padx=10, fill="x")

        ctk.CTkLabel(frame_formulario, text="Email:").pack(pady=(10,0), padx=10, anchor="w")
        self.entry_cliente_email = ctk.CTkEntry(frame_formulario)
        self.entry_cliente_email.pack(pady=5, padx=10, fill="x")

        frame_botones_cliente = ctk.CTkFrame(frame_formulario, fg_color="transparent")
        frame_botones_cliente.pack(pady=10, padx=10, fill="x", expand=True)
        frame_botones_cliente.grid_columnconfigure((0, 1), weight=1)

        self.boton_agregar_cliente = ctk.CTkButton(frame_botones_cliente, text="Agregar", command=self.agregar_cliente, **self.button_styles['primary'])
        self.boton_agregar_cliente.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.boton_actualizar_cliente = ctk.CTkButton(frame_botones_cliente, text="Actualizar", command=self.actualizar_cliente, **self.button_styles['primary'])
        self.boton_actualizar_cliente.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.boton_actualizar_cliente.configure(state="disabled")

        self.boton_limpiar_cliente = ctk.CTkButton(frame_botones_cliente, text="Limpiar", command=self.limpiar_campos_cliente)
        self.boton_limpiar_cliente.grid(row=1, column=0, columnspan=2, padx=5, pady=(5,0), sticky="ew")

        # --- Treeview ---
        self.tree_clientes = ttk.Treeview(frame_treeview, columns=("ID", "Nombre", "Apellido", "Email"), show="headings")
        self.tree_clientes.heading("ID", text="ID")
        self.tree_clientes.heading("Nombre", text="Nombre")
        self.tree_clientes.heading("Apellido", text="Apellido")
        self.tree_clientes.heading("Email", text="Email")
        self.tree_clientes.column("ID", width=30)
        self.tree_clientes.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.tree_clientes.bind("<<TreeviewSelect>>", self.seleccionar_cliente)

        self.boton_eliminar_cliente = ctk.CTkButton(frame_treeview, text="Eliminar Cliente Seleccionado", command=self.eliminar_cliente, **self.button_styles['danger'])
        self.boton_eliminar_cliente.grid(row=1, column=0, pady=10, padx=5, sticky="ew")

        self.cargar_clientes_en_treeview()

    def cargar_clientes_en_treeview(self):
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        
        session = get_db_session()
        try:
            clientes = cliente_crud.get_all_clientes(session)
            self.clientes.clear()
            for cliente in clientes:
                self.tree_clientes.insert("", "end", values=(cliente.id, cliente.nombre, cliente.apellido, cliente.email))
                self.clientes[cliente.id] = cliente
        finally:
            session.close()

    def seleccionar_cliente(self, event=None):
        seleccion = self.tree_clientes.selection()
        if not seleccion:
            self.limpiar_campos_cliente()
            return

        item = self.tree_clientes.item(seleccion[0])
        cliente_id, nombre, apellido, email = item['values']

        self.limpiar_campos_cliente()
        self.entry_cliente_nombre.insert(0, nombre)
        self.entry_cliente_apellido.insert(0, apellido)
        self.entry_cliente_email.insert(0, email)

        self.boton_agregar_cliente.configure(state="disabled")
        self.boton_actualizar_cliente.configure(state="normal")

    def limpiar_campos_cliente(self):
        self.entry_cliente_nombre.delete(0, 'end')
        self.entry_cliente_apellido.delete(0, 'end')
        self.entry_cliente_email.delete(0, 'end')
        self.tree_clientes.selection_remove(self.tree_clientes.selection())
        self.boton_agregar_cliente.configure(state="normal")
        self.boton_actualizar_cliente.configure(state="disabled")

    def validar_email(self, email):
        # Patrón simple para validación de email
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        CTkMessagebox(title="Error de Validación", message="El formato del email no es válido.")
        return False

    def agregar_cliente(self):
        nombre = self.entry_cliente_nombre.get().strip()
        apellido = self.entry_cliente_apellido.get().strip()
        email = self.entry_cliente_email.get().strip()

        if not all([nombre, apellido, email]):
            CTkMessagebox(title="Error", message="Todos los campos son obligatorios.", icon="warning")
            return
        
        if not self.validar_email(email):
            return

        session = get_db_session()
        try:
            cliente_crud.create_cliente(session, nombre, apellido, email)
            CTkMessagebox(title="Éxito", message="Cliente agregado correctamente.", icon="info")
            self.cargar_clientes_en_treeview()
            self.limpiar_campos_cliente()
        except IntegrityError:
            CTkMessagebox(title="Error de Duplicado", message=f"El email '{email}' ya está registrado.", icon="error")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Ocurrió un error: {e}", icon="error")
        finally:
            session.close()

    def actualizar_cliente(self):
        seleccion = self.tree_clientes.selection()
        if not seleccion:
            return

        cliente_id = int(self.tree_clientes.item(seleccion[0])['values'][0])
        nombre = self.entry_cliente_nombre.get().strip()
        apellido = self.entry_cliente_apellido.get().strip()
        email = self.entry_cliente_email.get().strip()

        if not all([nombre, apellido, email]):
            CTkMessagebox(title="Error", message="Todos los campos son obligatorios.", icon="warning")
            return

        if not self.validar_email(email):
            return

        session = get_db_session()
        try:
            cliente_crud.update_cliente(session, cliente_id, nombre, apellido, email)
            CTkMessagebox(title="Éxito", message="Cliente actualizado correctamente.", icon="info")
            self.cargar_clientes_en_treeview()
            self.limpiar_campos_cliente()
        except IntegrityError:
            CTkMessagebox(title="Error de Duplicado", message=f"El email '{email}' ya está registrado por otro cliente.", icon="error")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Ocurrió un error: {e}", icon="error")
        finally:
            session.close()

    def eliminar_cliente(self):
        seleccion = self.tree_clientes.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Seleccione un cliente para eliminar.", icon="warning")
            return

        cliente_id = int(self.tree_clientes.item(seleccion[0])['values'][0])
        
        msg = CTkMessagebox(title="Confirmar Eliminación", 
                            message="¿Está seguro de que desea eliminar a este cliente? Esta acción no se puede deshacer.",
                            icon="warning", option_1="No", option_2="Sí")
        if msg.get() != "Sí":
            return

        session = get_db_session()
        try:
            if not cliente_crud.delete_cliente(session, cliente_id):
                CTkMessagebox(title="Acción no permitida", message="No se puede eliminar un cliente que tiene pedidos asociados.", icon="error")
                return

            CTkMessagebox(title="Éxito", message="Cliente eliminado correctamente.", icon="info")
            self.cargar_clientes_en_treeview()
            self.limpiar_campos_cliente()
        except Exception as e:
            session.rollback()
            CTkMessagebox(title="Error", message=f"Ocurrió un error: {e}", icon="error")
        finally:
            session.close()

    def configurar_pestana3(self): # se crea la funcion para configurar la pestaña 3
        label = ctk.CTkLabel(self.tab3, text="Carga de archivo CSV") # se crea la etiqueta
        label.pack(pady=20) # se empaqueta la etiqueta
        boton_cargar_csv = ctk.CTkButton(
            self.tab3, 
            text="Cargar CSV",
            command=self.cargar_csv,
            **self.button_styles['primary']
        )
        # se crea el boton de carga el csv

        boton_cargar_csv.pack(pady=10) # se empaqueta el boton

        self.frame_tabla_csv = ctk.CTkFrame(self.tab3) # se crea el frame de la tabla csv
        self.frame_tabla_csv.pack(fill="both", expand=True, padx=10, pady=10) # se empaqueta el frame
        self.df_csv = None   # se crea el dataframe vacio
        self.tabla_csv = None # se crea la tabla vacia

        self.boton_agregar_stock = ctk.CTkButton(self.frame_tabla_csv, text="Agregar al Stock") # se crea el boton para agragar el stock
        self.boton_agregar_stock.pack(side="bottom", pady=10) # se empaqueta el boton
 
    def agregar_csv_al_stock(self): # se crea la funcion para agregra el csv al stock
        if self.df_csv is None: # se verifica el dataframe
            CTkMessagebox(title="Error", message="Primero debes cargar un archivo CSV.", icon="warning") # mensaje de error
            return # retorna el mensaje de error

        if 'nombre' not in self.df_csv.columns or 'cantidad' not in self.df_csv.columns: # verifica la columnas del csv
            CTkMessagebox(title="Error", message="El CSV debe tener columnas 'nombre' y 'cantidad'.", icon="warning") # mensaje de error
            return # retorna el mensaje de error
        
        for _, row in self.df_csv.iterrows(): # recorre las filas dell csv
            nombre = str(row['nombre'])
            cantidad = Decimal(str(row['cantidad']))
            unidad = str(row['unidad']) 
            # si no existe la unidad se pone unid por defecto
            ingrediente = Ingrediente(nombre=nombre,unidad=unidad,cantidad=cantidad) # se crea el ingredientes con sus datos
            self.stock.agregar_ingrediente(ingrediente) # se agrega el ingrediente al stock
        CTkMessagebox(title="Stock Actualizado", message="Ingredientes agregados al stock correctamente.", icon="info")
        # mensaje de exito
        self.actualizar_treeview()   # se actualiza la pantalla

    def cargar_csv(self): # se crea la funcion para cargar el csv
        """
        Carga un archivo CSV con ingredientes.
        Registra todas las acciones en logs centralizados.
        """
        logger.info("Iniciando carga de archivo CSV")
        
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("CSV files", "*.csv")]
        )
        # se selecciona el archivo csv
       
        if archivo: # si se selecciona un archivo
            logger.info(f"Archivo seleccionado: {archivo}")
            try: # se intenta cargar el archivo
                self.df_csv = pd.read_csv(archivo) # se carga el archivo csv
                logger.debug(f"CSV cargado con {len(self.df_csv)} filas")
                
                if not all(col in self.df_csv.columns for col in ['nombre', 'unidad', 'cantidad']): # verifica la columnas del csv
                    logger.error("CSV inválido: falta columnas requeridas (nombre, unidad, cantidad)")
                    CTkMessagebox(title="Error", message="El archivo CSV debe contener las columnas: nombre, unidad y cantidad", icon="warning")
                    # se detiene la carga del archivo
                    return # retorna el mensaje de error
                
                logger.info("CSV validado correctamente con columnas: nombre, unidad, cantidad")
                self.mostrar_dataframe_en_tabla(self.df_csv) # se muestea el dataframe en la tabla
                self.boton_agregar_stock.configure(command=self.agregar_csv_al_stock)
            except Exception as e:
                logger.error(f"Error al cargar CSV: {str(e)}")
                CTkMessagebox(title="Error", message=f"Error al cargar el archivo CSV: {str(e)}", icon="warning")
        else:
            logger.info("Carga de CSV cancelada por usuario")
        
    def mostrar_dataframe_en_tabla(self, df):
        if self.tabla_csv:
            self.tabla_csv.destroy()

        self.tabla_csv = ttk.Treeview(self.frame_tabla_csv, columns=list(df.columns), show="headings")
        for col in df.columns:
            self.tabla_csv.heading(col, text=col)
            self.tabla_csv.column(col, width=100, anchor="center")


        for _, row in df.iterrows():
            self.tabla_csv.insert("", "end", values=list(row))

        self.tabla_csv.pack(expand=True, fill="both", padx=10, pady=10)

    def actualizar_treeview_pedido(self):
        for item in self.treeview_menu.get_children():
            self.treeview_menu.delete(item)

        for menu in self.pedido.menus.values():
            self.treeview_menu.insert("", "end", values=(menu.nombre, menu.cantidad, f"${menu.precio:.2f}"))
            
    def _configurar_pestana_crear_menu(self):
        contenedor = ctk.CTkFrame(self.tab4)
        contenedor.pack(expand=True, fill="both", padx=10, pady=10)

        boton_menu = ctk.CTkButton(
            contenedor,
            text="Generar Carta (PDF)",
            command=self.generar_y_mostrar_carta_pdf
        )
        boton_menu.pack(pady=10)

        self.pdf_frame_carta = ctk.CTkFrame(contenedor)
        self.pdf_frame_carta.pack(expand=True, fill="both", padx=10, pady=10)

        self.pdf_viewer_carta = None
    def generar_y_mostrar_carta_pdf(self):
        try:
            pdf_path = "carta.pdf"
            create_menu_pdf(self.menus,  # type: ignore
                pdf_path,
                titulo_negocio="Restaurante",
                subtitulo="Carta Primavera 2025",
                moneda="$")
            
            if self.pdf_viewer_carta is not None:
                try:
                    self.pdf_viewer_carta.pack_forget()
                    self.pdf_viewer_carta.destroy()
                except Exception:
                    pass
                self.pdf_viewer_carta = None

            abs_pdf = os.path.abspath(pdf_path)
            self.pdf_viewer_carta = CTkPDFViewer(self.pdf_frame_carta, file=abs_pdf)
            self.pdf_viewer_carta.pack(expand=True, fill="both")

        except Exception as e:
            CTkMessagebox(title="Error", message=f"No se pudo generar/mostrar la carta.\n{e}", icon="warning")

    def _configurar_pestana_ver_boleta(self):
        contenedor = ctk.CTkFrame(self.tab5)
        contenedor.pack(expand=True, fill="both", padx=10, pady=10)
    
        boton_boleta = ctk.CTkButton(
            contenedor,
            text="Mostrar Boleta (PDF)",
            command=self.mostrar_boleta
        )
        boton_boleta.pack(pady=10)
    
        self.pdf_frame_boleta = ctk.CTkFrame(contenedor)
        self.pdf_frame_boleta.pack(expand=True, fill="both", padx=10, pady=10)
    
        self.pdf_viewer_boleta = None
        

    def mostrar_boleta(self):
        """Muestra la boleta más reciente en el visor PDF."""
        try:
            # Verificar si existe el directorio de boletas
            if not os.path.exists("boletas"):
                CTkMessagebox(title="Error", message="No hay boletas generadas para mostrar.", icon="warning")
                return

            # Obtener la lista de boletas y ordenarlas por fecha
            boletas = [f for f in os.listdir("boletas") if f.startswith("boleta_")]
            if not boletas:
                CTkMessagebox(title="Error", message="No hay boletas generadas para mostrar.", icon="warning")
                return

            # Obtener la boleta más reciente
            ultima_boleta = max(boletas)  # Como el formato incluye timestamp, max() dará la más reciente
            ruta_boleta = os.path.join("boletas", ultima_boleta)

            if self.pdf_viewer_boleta is not None:
                self.pdf_viewer_boleta.pack_forget()
                self.pdf_viewer_boleta.destroy()
            
            abs_pdf = os.path.abspath(ruta_boleta)
            self.pdf_viewer_boleta = CTkPDFViewer(self.pdf_frame_boleta, file=abs_pdf)
            self.pdf_viewer_boleta.pack(expand=True, fill="both")
            
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error al mostrar la boleta: {str(e)}", icon="warning")

    def configurar_pestana1(self):
        # Dividir la Pestaña 1 en dos frames
        frame_formulario = ctk.CTkFrame(self.tab1)
        frame_formulario.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        frame_treeview = ctk.CTkFrame(self.tab1)
        frame_treeview.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Formulario en el primer frame
        label_nombre = ctk.CTkLabel(frame_formulario, text="Nombre del Ingrediente:")
        label_nombre.pack(pady=5)
        self.entry_nombre = ctk.CTkEntry(frame_formulario)
        self.entry_nombre.pack(pady=5)

        label_cantidad = ctk.CTkLabel(frame_formulario, text="Unidad:")
        label_cantidad.pack(pady=5)
        self.combo_unidad = ctk.CTkComboBox(frame_formulario, values=["unid"], state="readonly")
        self.combo_unidad.set("unid")
        self.combo_unidad.pack(pady=5)

        label_cantidad = ctk.CTkLabel(frame_formulario, text="Cantidad:")
        label_cantidad.pack(pady=5)
        self.entry_cantidad = ctk.CTkEntry(frame_formulario)
        self.entry_cantidad.pack(pady=5)

        self.boton_ingresar = ctk.CTkButton(
            frame_formulario,
            text="Ingresar Ingrediente",
            **self.button_styles['secondary']
        )
        self.boton_ingresar.configure(command=self.ingresar_ingrediente)
        self.boton_ingresar.pack(pady=10)

        self.boton_eliminar = ctk.CTkButton(
            frame_treeview,
            text="Eliminar Ingrediente",
            **self.button_styles['danger']
        )
        self.boton_eliminar.configure(command=self.eliminar_ingrediente)
        self.boton_eliminar.pack(pady=10)

        self.boton_editar_stock = ctk.CTkButton(
            frame_treeview,
            text="Editar Stock",
            command=self.editar_stock_ingrediente,
            **self.button_styles['primary']
        )
        self.boton_editar_stock.pack(pady=10)

        self.tree = ttk.Treeview(self.tab1, columns=("Nombre", "Unidad","Cantidad"), show="headings",height=25)
        
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Unidad", text="Unidad")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.boton_generar_menu = ctk.CTkButton(frame_treeview, text="Generar Menú", command=self.generar_menus)
        self.boton_generar_menu.pack(pady=10)

    def tarjeta_click(self, event, menu):
        # Verificar stock
        faltantes = []
        for ing_necesario in menu.ingredientes:
            encontrado = False
            for ing_stock in self.stock.lista_ingredientes.values():
                if ing_necesario.ingrediente.nombre == ing_stock.nombre:
                    encontrado = True
                    if float(ing_stock.cantidad) < float(ing_necesario.cantidad_necesaria):
                        faltantes.append(f"{ing_necesario.ingrediente.nombre}: necesita {ing_necesario.cantidad_necesaria} {ing_necesario.ingrediente.unidad}, hay {ing_stock.cantidad} {ing_stock.unidad}")
                    break
            if not encontrado:
                faltantes.append(f"{ing_necesario.ingrediente.nombre}: necesita {ing_necesario.cantidad_necesaria} {ing_necesario.ingrediente.unidad}, no hay en stock")

        if faltantes:
            mensaje = f"No hay suficientes ingredientes para preparar el menú '{menu.nombre}'.\n\nIngredientes necesarios:\n"
            mensaje += "\n".join(faltantes)
            CTkMessagebox(title="Stock Insuficiente", 
                         message=mensaje, 
                         icon="warning")
            return
        
        # Reservar ingredientes
        self.stock.reservar_ingredientes(menu.ingredientes)
        
        # Convertir models.Menu a CrearMenu
        ingredientes_para_pedido = [
            Ingrediente(
                nombre=mi.ingrediente.nombre,
                unidad=mi.ingrediente.unidad,
                cantidad=mi.cantidad_necesaria
            ) for mi in menu.ingredientes
        ]
        menu_para_pedido = CrearMenu(
            id=menu.id,
            nombre=menu.nombre,
            ingredientes=ingredientes_para_pedido,
            precio=menu.precio,
            icono_path=menu.icono_path,
        )

        # Agregar al pedido
        self.pedido.agregar_menu(menu_para_pedido)
        self.actualizar_treeview_pedido()
        total = self.pedido.calcular_total()
        self.label_total.configure(text=f"Total: ${total:.2f}")
        
        # Actualizar vista del stock
        self.actualizar_treeview()
    
    def cargar_icono_menu(self, ruta_icono):
        imagen = Image.open(ruta_icono)
        icono_menu = ctk.CTkImage(imagen, size=(64, 64))
        return icono_menu

    def generar_menus(self):
        # Limpiar el frame de tarjetas existente SOLO si es necesario
        for widget in self.tarjetas_frame.winfo_children():
            widget.destroy()
        
        # Recrear todas las tarjetas
        self.menus_creados.clear()
        session = get_db_session()
        try:
            self.menus = menu_crud.get_all_menus(session)
            for menu in self.menus:
                self.crear_tarjeta(menu)
                self.menus_creados.add(menu)
        finally:
            session.close()
            
    def actualizar_menus(self):
        """Actualiza la visualización de los menús cuando cambia el stock (optimizado para evitar parpadeos)"""
        # Solo regenerar si no hay menús creados aún
        if not hasattr(self, 'menus_creados') or not self.menus_creados:
            self.generar_menus()
        # Si ya existen menús, no hacer nada para evitar parpadeos

    def eliminar_menu(self):
        seleccion = self.treeview_menu.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Por favor, seleccione uno o más menús para eliminar.", icon="warning")
            return

        # Preguntar confirmación si se seleccionaron múltiples menús
        if len(seleccion) > 1:
            msg = CTkMessagebox(
                title="Confirmar eliminación",
                message=f"¿Estás seguro de que deseas eliminar {len(seleccion)} menús seleccionados?",
                icon="warning",
                option_1="Sí",
                option_2="No"
            )
            if msg.get() != "Sí":
                return

        # Procesar cada menú seleccionado
        for sel in seleccion:
            item = self.treeview_menu.item(sel)
            nombre_menu = item['values'][0]
            
            # Encontrar el menú que se va a eliminar
            menu_a_eliminar = None
            for menu in self.pedido.menus.values():
                if menu.nombre == nombre_menu:
                    menu_a_eliminar = menu
                    break
                    
            if menu_a_eliminar:
                # Ajustar la cantidad de ingredientes a devolver
                ingredientes_ajustados = []
                for ingrediente in menu_a_eliminar.ingredientes:
                    ing_ajustado = Ingrediente(
                        nombre=ingrediente.nombre,
                        unidad=ingrediente.unidad,
                        cantidad=ingrediente.cantidad * menu_a_eliminar.cantidad
                    )
                    ingredientes_ajustados.append(ing_ajustado)
                
                # Devolver los ingredientes al stock
                self.stock.devolver_ingredientes(ingredientes_ajustados)
                
                # Eliminar del pedido
                self.pedido.eliminar_menu(nombre_menu)
        
        # Actualizar vistas
        self.actualizar_treeview_pedido()
        self.actualizar_treeview()
        total = self.pedido.calcular_total()
        self.label_total.configure(text=f"Total: ${total:.2f}")

    def eliminar_todo(self):
        if not self.pedido.menus:
            CTkMessagebox(title="Error", message="No hay menús en el pedido.", icon="warning")
            return

        msg = CTkMessagebox(
            title="Confirmar eliminación",
            message="¿Estás seguro de que deseas eliminar todo el pedido?",
            icon="warning",
            option_1="Sí",
            option_2="No"
        )
        if msg.get() != "Sí":
            return

        # Devolver todos los ingredientes al stock
        for menu in self.pedido.menus.values():
            ingredientes_ajustados = []
            for ingrediente in menu.ingredientes:
                ing_ajustado = Ingrediente(
                    nombre=ingrediente.nombre,
                    unidad=ingrediente.unidad,
                    cantidad=ingrediente.cantidad * menu.cantidad
                )
                ingredientes_ajustados.append(ing_ajustado)
            self.stock.devolver_ingredientes(ingredientes_ajustados)

        # Crear un nuevo pedido vacío
        self.pedido = Pedido()
        
        # Actualizar vistas
        self.actualizar_treeview_pedido()
        self.actualizar_treeview()
        self.label_total.configure(text="Total: $0.00")

    def generar_boleta(self):
        """
        Genera boleta de pedido con todas las validaciones y logging.
        Registra cada paso del proceso en el archivo de log.
        """
        # Validar que se haya seleccionado un cliente primero
        cliente_seleccionado = self.combo_clientes_pedido.get()
        if not cliente_seleccionado or cliente_seleccionado == "Seleccione un cliente":
            logger.warning("Intento de generar boleta sin cliente seleccionado")
            CTkMessagebox(
                title="Error - Cliente Requerido", 
                message="⚠️ Debes seleccionar un cliente antes de generar la boleta.", 
                icon="warning"
            )
            return

        if not self.pedido.menus:
            logger.warning("Intento de generar boleta con pedido vacio")
            CTkMessagebox(title="Error", message="No hay elementos en el pedido para generar la boleta.", icon="warning")
            return
        
        # Obtener el ID del cliente a partir del texto del combobox
        try:
            cliente_id = int(cliente_seleccionado.split(" - ")[0])
            logger.info(f"Generando boleta para cliente ID: {cliente_id}")
        except (ValueError, IndexError):
            logger.error(f"Error: Cliente seleccionado invalido: {cliente_seleccionado}")
            CTkMessagebox(title="Error", message="El cliente seleccionado no es válido.", icon="warning")
            return

        session = get_db_session()
        try:
            items_data = []
            total_pedido = 0
            for menu in self.pedido.menus.values():
                items_data.append({
                    'menu_id': menu.id,
                    'cantidad': menu.cantidad,
                    'precio_unitario': menu.precio
                })
                total_pedido += menu.precio * menu.cantidad
                logger.debug(f"Item en boleta: {menu.nombre} x {menu.cantidad} = ${menu.precio * menu.cantidad:.2f}")
            
            nuevo_pedido = pedido_crud.create_pedido(session, cliente_id, items_data)
            logger.info(f"Pedido creado en BD con ID: {nuevo_pedido.id}")
            
            boleta = BoletaFacade(nuevo_pedido.id)
            pdf_path = boleta.generar_boleta()
            logger.info(f"Boleta generada en: {pdf_path}")

            if not os.path.exists(pdf_path):
                logger.error(f"Archivo de boleta no encontrado: {pdf_path}")
                raise FileNotFoundError(f"No se pudo encontrar el archivo de la boleta: {pdf_path}")
                
            if self.pdf_viewer_boleta is not None:
                self.pdf_viewer_boleta.pack_forget()
                self.pdf_viewer_boleta.destroy()
            
            abs_pdf = os.path.abspath(pdf_path)
            self.pdf_viewer_boleta = CTkPDFViewer(self.pdf_frame_boleta, file=abs_pdf)
            self.pdf_viewer_boleta.pack(expand=True, fill="both")
            
            self.pedido = Pedido()
            self.actualizar_treeview_pedido()
            self.label_total.configure(text="Total: $0.00")
            
            logger.info(f"Boleta procesada exitosamente - Total: ${total_pedido:.2f}")
            CTkMessagebox(
                title="Exito",
                message=f"Boleta generada exitosamente y guardada en:\n{abs_pdf}",
                icon="info"
            )
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error al generar boleta: {str(e)}", exc_info=True)
            CTkMessagebox(title="Error", message=f"Error al generar la boleta: {str(e)}", icon="warning")
        finally:
            session.close()

    def configurar_pestana2(self):
        # Frame principal de la pestaña de Pedido
        frame_principal_pedido = ctk.CTkFrame(self.tab2)
        frame_principal_pedido.pack(fill="both", expand=True)
        frame_principal_pedido.grid_rowconfigure(2, weight=1)  # El frame de tarjetas se expande
        frame_principal_pedido.grid_columnconfigure(0, weight=1)

        # --- Frame superior para selección de cliente ---
        frame_cliente = ctk.CTkFrame(frame_principal_pedido)
        frame_cliente.pack(fill="x", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(frame_cliente, text="Seleccionar Cliente:").pack(side="left", padx=(10, 5))
        
        self.combo_clientes_pedido = ctk.CTkComboBox(frame_cliente, state="readonly", values=["Seleccione un cliente"])
        self.combo_clientes_pedido.pack(side="left", expand=True, fill="x", padx=(0, 10))
        self.combo_clientes_pedido.set("Seleccione un cliente")

        # --- Frame para las tarjetas de menú ---
        frame_superior = ctk.CTkFrame(frame_principal_pedido)
        frame_superior.pack(fill="both", expand=True, padx=10, pady=5)

        self.tarjetas_frame = ctk.CTkScrollableFrame(frame_superior, orientation="horizontal", label_text="Menús Disponibles")
        self.tarjetas_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # --- Frame intermedio para controles y total ---
        frame_intermedio = ctk.CTkFrame(frame_principal_pedido)
        frame_intermedio.pack(fill="x", padx=10, pady=5)

        # Frame para los botones de control
        frame_botones = ctk.CTkFrame(frame_intermedio)
        frame_botones.pack(side="left", expand=True, fill="x", padx=10)

        self.boton_eliminar_menu = ctk.CTkButton(
            frame_botones, 
            text="Eliminar Seleccionados", 
            command=self.eliminar_menu,
            **self.button_styles['danger']
        )
        self.boton_eliminar_menu.pack(side="left", padx=5)

        self.boton_eliminar_todo = ctk.CTkButton(
            frame_botones, 
            text="Limpiar Pedido", 
            command=self.eliminar_todo,
            **self.button_styles['danger']
        )
        self.boton_eliminar_todo.pack(side="left", padx=5)

        self.label_total = ctk.CTkLabel(frame_intermedio, text="Total: $0.00", anchor="e", font=("Helvetica", 12, "bold"))
        self.label_total.pack(side="right", padx=10)

        # --- Frame inferior para el detalle del pedido y botón de boleta ---
        frame_inferior = ctk.CTkFrame(frame_principal_pedido)
        frame_inferior.pack(fill="both", expand=True, padx=10, pady=10)
        frame_inferior.grid_rowconfigure(0, weight=1)  # El treeview se expande
        frame_inferior.grid_columnconfigure(0, weight=1)

        # Frame con scroll para el treeview
        frame_scroll = ctk.CTkFrame(frame_inferior)
        frame_scroll.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        frame_scroll.grid_rowconfigure(0, weight=1)
        frame_scroll.grid_columnconfigure(0, weight=1)

        self.treeview_menu = ttk.Treeview(frame_scroll, columns=("Nombre", "Cantidad", "Precio Unitario"), show="headings", height=8)
        self.treeview_menu.heading("Nombre", text="Nombre del Menú")
        self.treeview_menu.heading("Cantidad", text="Cantidad")
        self.treeview_menu.heading("Precio Unitario", text="Precio Unitario")
        self.treeview_menu.grid(row=0, column=0, sticky="nsew")

        # Scrollbar para el treeview
        scrollbar = ttk.Scrollbar(frame_scroll, orient="vertical", command=self.treeview_menu.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.treeview_menu["yscroll"] = scrollbar.set

        self.boton_generar_boleta = ctk.CTkButton(
            frame_inferior,
            text="Generar Boleta",
            command=self.generar_boleta,
            **self.button_styles['primary']
        )
        self.boton_generar_boleta.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

    def actualizar_clientes_combobox(self):
        session = get_db_session()
        try:
            clientes = session.query(Cliente).order_by(Cliente.nombre).all()
            # Usamos map y lambda para formatear la lista de clientes
            lista_formateada = list(map(lambda c: f"{c.id} - {c.nombre} {c.apellido}", clientes))
            if not lista_formateada:
                lista_formateada = ["No hay clientes registrados"]
                self.combo_clientes_pedido.set(lista_formateada[0])
            else:
                lista_formateada.insert(0, "Seleccione un cliente")
                # Solo cambiamos al valor por defecto si el actual no es válido
                if self.combo_clientes_pedido.get() not in lista_formateada:
                    self.combo_clientes_pedido.set(lista_formateada[0])

            self.combo_clientes_pedido.configure(values=lista_formateada)
        finally:
            session.close()

    def crear_tarjeta(self, menu):
        # Usamos filter para encontrar si el menú ya fue creado
        if any(filter(lambda m: m.nombre == menu.nombre, self.menus_creados)):
             pass # Opcional: se podría actualizar en lugar de saltar

        # Verificar si hay suficientes ingredientes
        hay_ingredientes = self.stock.verificar_ingredientes_suficientes(menu.ingredientes)

        # Configurar el estilo de la tarjeta según disponibilidad
        tarjeta = ctk.CTkFrame(
            self.tarjetas_frame,
            corner_radius=10,
            border_width=1,
            border_color="#4CAF50" if hay_ingredientes else "#FF0000",
            width=120, # Ancho aumentado para mejor visualización
            height=150, # Alto aumentado
            fg_color="gray17" if hay_ingredientes else "gray30",
        )
        
        # Usamos lambda para el evento click
        if hay_ingredientes:
            tarjeta.bind("<Button-1>", lambda event, m=menu: self.tarjeta_click(event, m))
            tarjeta.bind("<Enter>", lambda event: tarjeta.configure(border_color="#1976D2"))
            tarjeta.bind("<Leave>", lambda event: tarjeta.configure(border_color="#4CAF50"))

        if getattr(menu, "icono_path", None):
            try:
                icono = self.cargar_icono_menu(menu.icono_path)
                imagen_label = ctk.CTkLabel(tarjeta, image=icono, text="", bg_color="transparent")
                imagen_label.pack(pady=(10, 5), padx=10)
                if hay_ingredientes:
                    imagen_label.bind("<Button-1>", lambda event, m=menu: self.tarjeta_click(event, m))
            except Exception as e:
                print(f"No se pudo cargar la imagen '{menu.icono_path}': {e}")

        nombre_texto = f"{menu.nombre}\n${menu.precio}"
        if not hay_ingredientes:
            nombre_texto += "\n(Agotado)"
        
        texto_label = ctk.CTkLabel(
            tarjeta,
            text=nombre_texto,
            text_color="white" if hay_ingredientes else "gray60",
            font=("Helvetica", 11),
            bg_color="transparent",
        )
        texto_label.pack(pady=(0, 10), padx=5)
        if hay_ingredientes:
            texto_label.bind("<Button-1>", lambda event, m=menu: self.tarjeta_click(event, m))
        
        # Añadir la tarjeta al grid dinámicamente
        num_tarjetas = len(self.tarjetas_frame.winfo_children())
        tarjeta.grid(row=0, column=num_tarjetas, padx=10, pady=10)


    def validar_nombre(self, nombre):
        if re.match(r"^[a-zA-Z\s]+$", nombre):
            return True
        else:
            CTkMessagebox(title="Error de Validación", message="El nombre debe contener solo letras y espacios.", icon="warning")
            return False

    def validar_cantidad(self, cantidad):
        if cantidad.isdigit():
            return True
        else:
            CTkMessagebox(title="Error de Validación", message="La cantidad debe ser un número entero positivo.", icon="warning")
            return False

    def ingresar_ingrediente(self):
        """
        Ingresa un nuevo ingrediente al sistema con validación integrada.
        Usa validadores del patrón Template Method desde error_handler.
        """
        nombre = self.entry_nombre.get()
        unidad = self.combo_unidad.get()
        cantidad = self.entry_cantidad.get()

        # ════════════════════════════════════════════════════════════
        # VALIDACIÓN USANDO TEMPLATE METHOD
        # ════════════════════════════════════════════════════════════
        
        # Validar nombre
        validador_nombre = ValidadorNombre(longitud_minima=2)
        if not validador_nombre.validar(nombre):
            logger.warning(f"Intento de ingresar nombre inválido: '{nombre}'")
            CTkMessagebox(title="Error", message="El nombre debe tener al menos 2 caracteres", icon="warning")
            return
        
        # Validar cantidad
        validador_cantidad = ValidadorCantidad()
        if not validador_cantidad.validar(cantidad):
            logger.warning(f"Intento de ingresar cantidad inválida: '{cantidad}'")
            CTkMessagebox(title="Error", message="La cantidad debe ser un número positivo", icon="warning")
            return

        logger.info(f"Ingresando nuevo ingrediente: {nombre} ({cantidad} {unidad})")

        session = get_db_session()
        try:
            ingrediente_existente = ingrediente_crud.get_ingrediente_by_name(session, nombre)
            if ingrediente_existente:
                # Actualizar cantidad si el ingrediente ya existe
                nueva_cantidad = ingrediente_existente.cantidad + Decimal(cantidad)
                ingrediente_crud.update_ingrediente(session, ingrediente_existente.id, nombre, unidad, nueva_cantidad)
                logger.info(f"Ingrediente '{nombre}' actualizado. Nueva cantidad: {nueva_cantidad} {unidad}")
            else:
                # Crear nuevo ingrediente
                ingrediente_crud.create_ingrediente(session, nombre, unidad, Decimal(cantidad))
                logger.info(f"Ingrediente '{nombre}' creado exitosamente. Cantidad: {cantidad} {unidad}")
            
            self.actualizar_treeview()

            # Limpiar campos
            self.entry_nombre.delete(0, 'end')
            self.entry_cantidad.delete(0, 'end')
            self.combo_unidad.set("unid")
        except Exception as e:
            session.rollback()
            logger.error(f"Error al ingresar ingrediente: {str(e)}")
            CTkMessagebox(title="Error", message=f"Ocurrió un error: {e}", icon="error")
        finally:
            session.close()

    def eliminar_ingrediente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Por favor, seleccione un ingrediente para eliminar.", icon="warning")
            return

        item = self.tree.item(seleccion[0])
        nombre_ingrediente = item['values'][0]
        
        msg = CTkMessagebox(title="Confirmar Acción", 
                            message=f"¿Está seguro de que desea marcar '{nombre_ingrediente}' como agotado? "
                                    "Esto hará que los menús que lo utilizan no estén disponibles.",
                            icon="warning", option_1="No", option_2="Sí")
        if msg.get() != "Sí":
            return

        session = get_db_session()
        try:
            # Obtener el ingrediente de la base de datos
            ingrediente_db = ingrediente_crud.get_ingrediente_by_name(session, nombre_ingrediente)
            
            if ingrediente_db:
                # Actualizar la cantidad a 0 en la base de datos
                ingrediente_crud.update_ingrediente(session, ingrediente_db.id, ingrediente_db.nombre, ingrediente_db.unidad, Decimal(0))
                
                # Actualizar la cantidad en el stock en memoria
                if nombre_ingrediente in self.stock.lista_ingredientes:
                    self.stock.lista_ingredientes[nombre_ingrediente].cantidad = Decimal(0)
                
                self.actualizar_treeview()
                CTkMessagebox(title="Éxito", message=f"El ingrediente '{nombre_ingrediente}' ha sido marcado como agotado.", icon="info")
            else:
                CTkMessagebox(title="Error", message="El ingrediente no se encontró en la base de datos.", icon="error")
        except Exception as e:
            session.rollback()
            CTkMessagebox(title="Error", message=f"Ocurrió un error inesperado: {e}", icon="error")
        finally:
            session.close()

    def editar_stock_ingrediente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Por favor, seleccione un ingrediente para editar.", icon="warning")
            return

        item = self.tree.item(seleccion[0])
        nombre_ingrediente = item['values'][0]
        cantidad_actual = item['values'][2]

        dialog = ctk.CTkInputDialog(
            text=f"Ingrese la nueva cantidad para '{nombre_ingrediente}' (actual: {cantidad_actual}):",
            title="Editar Stock"
        )
        nueva_cantidad_str = dialog.get_input()

        if nueva_cantidad_str is None or nueva_cantidad_str == "":
            return  # User cancelled or entered nothing

        try:
            nueva_cantidad = Decimal(nueva_cantidad_str)
            if nueva_cantidad < 0:
                CTkMessagebox(title="Error de Validación", message="La cantidad no puede ser negativa.", icon="warning")
                return
        except InvalidOperation:
            CTkMessagebox(title="Error de Validación", message="Por favor, ingrese un número válido para la cantidad.", icon="warning")
            return

        session = get_db_session()
        try:
            ingrediente_db = ingrediente_crud.get_ingrediente_by_name(session, nombre_ingrediente)
            if ingrediente_db:
                ingrediente_crud.update_ingrediente(session, ingrediente_db.id, ingrediente_db.nombre, ingrediente_db.unidad, nueva_cantidad)
                
                # Actualizar el stock en memoria
                if nombre_ingrediente in self.stock.lista_ingredientes:
                    self.stock.lista_ingredientes[nombre_ingrediente].cantidad = nueva_cantidad
                
                self.actualizar_treeview()
                CTkMessagebox(title="Éxito", message=f"Stock de '{nombre_ingrediente}' actualizado correctamente.", icon="info")
            else:
                CTkMessagebox(title="Error", message="El ingrediente no se encontró en la base de datos.", icon="error")
        except Exception as e:
            session.rollback()
            CTkMessagebox(title="Error", message=f"Ocurrió un error inesperado: {e}", icon="error")
        finally:
            session.close()

    def _configurar_pestana_estadisticas(self):
        self.statistics_tab_instance = StatisticsTab(self.tab_estadisticas)
        self.statistics_tab_instance.pack(expand=True, fill="both", padx=10, pady=10)

    def _configurar_pestana_reportes(self):
        """Configura la pestaña de Reportes con botones para generar reportes"""
        frame_principal = ctk.CTkFrame(self.tab_reportes)
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo = ctk.CTkLabel(
            frame_principal,
            text="Generador de Reportes",
            font=("Helvetica", 24, "bold")
        )
        titulo.pack(pady=20)
        
        # Descripción
        desc = ctk.CTkLabel(
            frame_principal,
            text="Exporta datos de pedidos en diferentes formatos",
            font=("Helvetica", 12)
        )
        desc.pack(pady=(0, 20))
        
        # Frame para botones
        frame_botones = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_botones.pack(pady=20)
        
        # Botón JSON
        btn_json = ctk.CTkButton(
            frame_botones,
            text="Exportar JSON",
            command=self.generar_reporte_json,
            width=200,
            height=50,
            font=("Helvetica", 14)
        )
        btn_json.pack(pady=10, padx=10, side="top")
        
        # Botón CSV
        btn_csv = ctk.CTkButton(
            frame_botones,
            text="Exportar CSV",
            command=self.generar_reporte_csv,
            width=200,
            height=50,
            font=("Helvetica", 14)
        )
        btn_csv.pack(pady=10, padx=10, side="top")
        
        # Botón HTML
        btn_html = ctk.CTkButton(
            frame_botones,
            text="Exportar HTML",
            command=self.generar_reporte_html,
            width=200,
            height=50,
            font=("Helvetica", 14)
        )
        btn_html.pack(pady=10, padx=10, side="top")
        
        # Frame para información
        frame_info = ctk.CTkFrame(frame_principal)
        frame_info.pack(fill="x", pady=20, padx=20)
        
        info_label = ctk.CTkLabel(
            frame_info,
            text="Los reportes se guardan en la carpeta 'reportes/'",
            font=("Helvetica", 11),
            text_color="gray"
        )
        info_label.pack(pady=10)

    def generar_reporte_json(self):
        """Genera reporte en formato JSON"""
        try:
            logger.info("Iniciando generacion de reporte JSON")
            archivo = generar_reporte("json", "pedidos")
            logger.info(f"Reporte JSON generado: {archivo}")
            
            CTkMessagebox(
                title="Exito",
                message=f"Reporte JSON generado exitosamente\n\nUbicacion: {archivo}",
                icon="info"
            )
        except Exception as e:
            logger.error(f"Error generando reporte JSON: {str(e)}", exc_info=True)
            CTkMessagebox(
                title="Error",
                message=f"Error al generar reporte: {str(e)}",
                icon="warning"
            )

    def generar_reporte_csv(self):
        """Genera reporte en formato CSV"""
        try:
            logger.info("Iniciando generacion de reporte CSV")
            archivo = generar_reporte("csv", "pedidos")
            logger.info(f"Reporte CSV generado: {archivo}")
            
            CTkMessagebox(
                title="Exito",
                message=f"Reporte CSV generado exitosamente\n\nUbicacion: {archivo}",
                icon="info"
            )
        except Exception as e:
            logger.error(f"Error generando reporte CSV: {str(e)}", exc_info=True)
            CTkMessagebox(
                title="Error",
                message=f"Error al generar reporte: {str(e)}",
                icon="warning"
            )

    def generar_reporte_html(self):
        """Genera reporte en formato HTML"""
        try:
            logger.info("Iniciando generacion de reporte HTML")
            archivo = generar_reporte("html", "pedidos")
            logger.info(f"Reporte HTML generado: {archivo}")
            
            CTkMessagebox(
                title="Exito",
                message=f"Reporte HTML generado exitosamente\n\nUbicacion: {archivo}",
                icon="info"
            )
        except Exception as e:
            logger.error(f"Error generando reporte HTML: {str(e)}", exc_info=True)
            CTkMessagebox(
                title="Error",
                message=f"Error al generar reporte: {str(e)}",
                icon="warning"
            )

if __name__ == "__main__":
    import customtkinter as ctk
    from tkinter import ttk

    ctk.set_appearance_mode("Dark")  
    ctk.set_default_color_theme("blue") 
    ctk.set_widget_scaling(1.0)
    ctk.set_window_scaling(1.0)

    app = AplicacionConPestanas()

    try:
        style = ttk.Style(app)   
        style.theme_use("clam")
    except Exception:
        pass

    try:
        app.mainloop()
    except KeyboardInterrupt:
        print("\n✓ Aplicación cerrada por el usuario (Ctrl+C)")
        app.quit()
        app.destroy()
