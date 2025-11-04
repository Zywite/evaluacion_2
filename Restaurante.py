from decimal import Decimal
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
from database import initialize_database
from Menu_catalog import get_default_menus, save_default_menus_to_db
#importamos todo lo que sea necesario

class AplicacionConPestanas(ctk.CTk): # se crea la clase de la aplicacion para las ventanas
    def __init__(self):
        initialize_database() # Initialize the database
        save_default_menus_to_db() # Populate default menus if not already in DB
        super().__init__() # se inicia la clase padre
        
        self.title("Gestión de ingredientes y pedidos") 
        self.geometry("870x700")
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
                'font': ('Helvetica', 12)
                #tamaño de fuente
            },
            'secondary': { #estilo secundario
                'fg_color': "#4CAF50",  # Verde material
                'hover_color': "#388E3C",  # Verde más oscuro
                'text_color': "white", #texto color blanco
                'corner_radius': 8, # borde redondeado
                'border_width': 0, # sin borde
                'font': ('Helvetica', 12) #tamaño de fuente
            },
            'danger': { #estilo de peligro
                'fg_color': "#F44336",  # Rojo material
                'hover_color': "#D32F2F",  # Rojo más oscuro
                'text_color': "white", #texto color blanco
                'corner_radius': 8, # borde redondeado
                'border_width': 0, # sin borde
                'font': ('Helvetica', 12) #tamaño de fuente
            }
        }

        self.stock = Stock() # se crea el stock
        self.menus_creados = set() #se crea un conjunto vacio para los menus creados
        self.pedido = Pedido() # se crea el pedido

        self.menus = get_default_menus()  # se obtienen los menus prederminados
  
        self.tabview = ctk.CTkTabview(self,command=self.on_tab_change) # se crea la pestaña
        self.tabview.pack(expand=True, fill="both", padx=10, pady=10) # se empaqueta la pestaña

        self.crear_pestanas() # se crean las pestañas

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
        if selected_tab in ["carga de ingredientes", "Stock", "Pedido", "Carta restorante", "Boleta"]: # si la pestaña es una de estas
            self.actualizar_treeview() # se actualiza la pantalla
    
    def crear_pestanas(self): # se crea la funcion de crear las pestañas
        self.tab3 = self.tabview.add("Carga de ingredientes")  
        self.tab1 = self.tabview.add("Stock")
        self.tab4 = self.tabview.add("Carta restorante")  
        self.tab2 = self.tabview.add("Pedido")
        self.tab5 = self.tabview.add("Boleta")
        # se crean las diferente pestañas con todos sus nombres
        self.configurar_pestana1()
        self.configurar_pestana2()
        self.configurar_pestana3()
        self._configurar_pestana_crear_menu()
        self._configurar_pestana_ver_boleta()
        # se configuran las pestañas con sus funciones
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
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("CSV files", "*.csv")]
        )
        # se selecciona el archivo csv
       
        if archivo: # si se selecciona un archivo
            try: # se intenta cargar el archivo
                self.df_csv = pd.read_csv(archivo) # se carga el archivo csv
                if not all(col in self.df_csv.columns for col in ['nombre', 'unidad', 'cantidad']): # verifica la columnas del csv
                    CTkMessagebox(title="Error", message="El archivo CSV debe contener las columnas: nombre, unidad y cantidad", icon="warning")
                    # se detiene la carga del archivo
                    return # retorna el mensaje de error
                self.mostrar_dataframe_en_tabla(self.df_csv) # se muestea el dataframe en la tabla
                self.boton_agregar_stock.configure(command=self.agregar_csv_al_stock)
            except Exception as e:
                CTkMessagebox(title="Error", message=f"Error al cargar el archivo CSV: {str(e)}", icon="warning")
        
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
            create_menu_pdf(self.menus, pdf_path,
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
                if ing_necesario.nombre == ing_stock.nombre:
                    encontrado = True
                    if float(ing_stock.cantidad) < float(ing_necesario.cantidad):
                        faltantes.append(f"{ing_necesario.nombre}: necesita {ing_necesario.cantidad} {ing_necesario.unidad}, hay {ing_stock.cantidad} {ing_stock.unidad}")
                    break
            if not encontrado:
                faltantes.append(f"{ing_necesario.nombre}: necesita {ing_necesario.cantidad} {ing_necesario.unidad}, no hay en stock")

        if faltantes:
            mensaje = f"No hay suficientes ingredientes para preparar el menú '{menu.nombre}'.\n\nIngredientes necesarios:\n"
            mensaje += "\n".join(faltantes)
            CTkMessagebox(title="Stock Insuficiente", 
                         message=mensaje, 
                         icon="warning")
            return
        
        # Reservar ingredientes
        self.stock.reservar_ingredientes(menu.ingredientes)
        
        # Agregar al pedido
        self.pedido.agregar_menu(menu)
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
        # Limpiar el frame de tarjetas existente
        for widget in self.tarjetas_frame.winfo_children():
            widget.destroy()
        
        # Recrear todas las tarjetas
        self.menus_creados.clear()
        for menu in self.menus:
            self.crear_tarjeta(menu)
            self.menus_creados.add(menu)
            
    def actualizar_menus(self):
        """Actualiza la visualización de los menús cuando cambia el stock"""
        if hasattr(self, 'menus_creados'):
            self.generar_menus()

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
        if not self.pedido.menus:
            CTkMessagebox(title="Error", message="No hay elementos en el pedido para generar la boleta.", icon="warning")
            return

        try:
            pedido_id = self.pedido.guardar_pedido()
            boleta = BoletaFacade(pedido_id)
            pdf_path = boleta.generar_boleta()  # Ahora devuelve directamente la ruta del archivo
            
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"No se pudo encontrar el archivo de la boleta: {pdf_path}")
                
            if self.pdf_viewer_boleta is not None:
                self.pdf_viewer_boleta.pack_forget()
                self.pdf_viewer_boleta.destroy()
            
            # Asegurarnos de usar la ruta absoluta
            abs_pdf = os.path.abspath(pdf_path)
            self.pdf_viewer_boleta = CTkPDFViewer(self.pdf_frame_boleta, file=abs_pdf)
            self.pdf_viewer_boleta.pack(expand=True, fill="both")
            
            # Limpiar el pedido actual
            self.pedido = Pedido()
            self.actualizar_treeview_pedido()
            self.label_total.configure(text="Total: $0.00")
            
            # Mostrar mensaje de éxito con la ubicación de la boleta
            CTkMessagebox(
                title="Éxito",
                message=f"Boleta generada exitosamente y guardada en:\n{abs_pdf}",
                icon="info"
            )
            
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error al generar la boleta: {str(e)}", icon="warning")

    def configurar_pestana2(self):
        frame_superior = ctk.CTkFrame(self.tab2)
        frame_superior.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        frame_intermedio = ctk.CTkFrame(self.tab2)
        frame_intermedio.pack(side="top", fill="x", padx=10, pady=5)

        self.tarjetas_frame = ctk.CTkFrame(frame_superior)
        self.tarjetas_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Frame para los botones de control
        frame_botones = ctk.CTkFrame(frame_intermedio)
        frame_botones.pack(side="right", padx=10)

        self.boton_eliminar_menu = ctk.CTkButton(
            frame_botones, 
            text="Eliminar Seleccionados", 
            command=self.eliminar_menu,
            **self.button_styles['danger']
        )
        self.boton_eliminar_menu.pack(side="right", padx=5)

        self.boton_eliminar_todo = ctk.CTkButton(
            frame_botones, 
            text="Limpiar Pedido", 
            command=self.eliminar_todo,
            **self.button_styles['danger']
        )
        self.boton_eliminar_todo.pack(side="right", padx=5)

        self.label_total = ctk.CTkLabel(frame_intermedio, text="Total: $0.00", anchor="e", font=("Helvetica", 12, "bold"))
        self.label_total.pack(side="right", padx=10)

        frame_inferior = ctk.CTkFrame(self.tab2)
        frame_inferior.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)

        self.treeview_menu = ttk.Treeview(frame_inferior, columns=("Nombre", "Cantidad", "Precio Unitario"), show="headings")
        self.treeview_menu.heading("Nombre", text="Nombre del Menú")
        self.treeview_menu.heading("Cantidad", text="Cantidad")
        self.treeview_menu.heading("Precio Unitario", text="Precio Unitario")
        self.treeview_menu.pack(expand=True, fill="both", padx=10, pady=10)

        self.boton_generar_boleta = ctk.CTkButton(
            frame_inferior,
            text="Generar Boleta",
            command=self.generar_boleta,
            **self.button_styles['primary']
        )
        self.boton_generar_boleta.pack(side="bottom",pady=10)

    def crear_tarjeta(self, menu):
        num_tarjetas = len(self.menus_creados)
        fila = 0
        columna = num_tarjetas

        # Verificar si hay suficientes ingredientes
        hay_ingredientes = self.stock.verificar_ingredientes_suficientes(menu.ingredientes)

        # Configurar el estilo de la tarjeta según disponibilidad
        tarjeta = ctk.CTkFrame(
            self.tarjetas_frame,
            corner_radius=10,
            border_width=1,
            border_color="#4CAF50" if hay_ingredientes else "#FF0000",
            width=64,
            height=140,
            fg_color="gray" if hay_ingredientes else "#808080",  # Gris más oscuro si no hay ingredientes
        )
        tarjeta.grid(row=fila, column=columna, padx=15, pady=15, sticky="nsew")

        # Solo permitir interacción si hay ingredientes suficientes
        if hay_ingredientes:
            tarjeta.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))
            tarjeta.bind("<Enter>", lambda event: tarjeta.configure(border_color="#FF0000"))
            tarjeta.bind("<Leave>", lambda event: tarjeta.configure(border_color="#4CAF50"))

        if getattr(menu, "icono_path", None):
            try:
                icono = self.cargar_icono_menu(menu.icono_path)
                imagen_label = ctk.CTkLabel(
                    tarjeta, 
                    image=icono, 
                    width=64, 
                    height=64, 
                    text="", 
                    bg_color="transparent"
                )
                
                # Aplicar efecto visual si no hay ingredientes suficientes
                if not hay_ingredientes:
                    imagen_label.configure(fg_color="gray50")  # Color semitransparente
                
                imagen_label.pack(anchor="center", pady=5, padx=10)
                if hay_ingredientes:
                    imagen_label.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))
            except Exception as e:
                print(f"No se pudo cargar la imagen '{menu.icono_path}': {e}")

        # Crear el texto del menú
        nombre_texto = f"{menu.nombre}"
        if not hay_ingredientes:
            nombre_texto += "\n(No disponible)"
        
        texto_label = ctk.CTkLabel(
            tarjeta,
            text=nombre_texto,
            text_color="black" if hay_ingredientes else "gray30",  # Texto más oscuro si no disponible
            font=("Helvetica", 12, "bold"),
            bg_color="transparent",
        )
        texto_label.pack(anchor="center", pady=1)
        if hay_ingredientes:
            texto_label.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))

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
        nombre = self.entry_nombre.get()
        unidad = self.combo_unidad.get()
        cantidad = self.entry_cantidad.get()

        if not self.validar_nombre(nombre) or not self.validar_cantidad(cantidad):
            return

        ingrediente = Ingrediente(nombre=nombre, unidad=unidad, cantidad=Decimal(cantidad))
        self.stock.agregar_ingrediente(ingrediente)
        self.actualizar_treeview()

        # Limpiar campos
        self.entry_nombre.delete(0, 'end')
        self.entry_cantidad.delete(0, 'end')
        self.combo_unidad.set("unid")

    def eliminar_ingrediente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Por favor, seleccione un ingrediente para eliminar.", icon="warning")
            return

        item = self.tree.item(seleccion[0])
        nombre_ingrediente = item['values'][0]
        
        self.stock.eliminar_ingrediente(nombre_ingrediente)
        self.actualizar_treeview()


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

    app.mainloop()