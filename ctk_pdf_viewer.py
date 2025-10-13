
from typing import Union
import customtkinter
from customtkinter import CTk, CTkFrame
from PIL import Image
import fitz
from threading import Thread
import math
import io
import os

class CTkPDFViewer(customtkinter.CTkScrollableFrame):
    def __init__(self,
                 master: Union[CTk, CTkFrame],
                 file: str,
                 page_width: int = 600,
                 page_height: int = 700,
                 page_separation_height: int = 2,
                 **kwargs):
        
        super().__init__(master, **kwargs)

        self.page_width = page_width
        self.page_height = page_height
        self.separation = page_separation_height
        self.pdf_images = []
        self.labels = []
        self.file = file

        self.percentage_view = 0
        self.percentage_load = customtkinter.StringVar()
        
        self.loading_message = customtkinter.CTkLabel(self, textvariable=self.percentage_load, justify="center")
        self.loading_message.pack(pady=10)

        self.loading_bar = customtkinter.CTkProgressBar(self, width=100)
        self.loading_bar.set(0)
        self.loading_bar.pack(side="top", fill="x", padx=10)

        self.after(250, self.start_process)

    def start_process(self):
        Thread(target=self.add_pages).start()
        
    def add_pages(self):
        """add images and labels"""
        try:
            self.percentage_bar = 0
            open_pdf = fitz.open(self.file)
            
            for page in open_pdf:
                # Convert PDF page to image using current PyMuPDF API
                pix = page.get_displaylist().get_pixmap(alpha=False)
                img = Image.open(io.BytesIO(pix.tobytes('ppm')))
                label_img = customtkinter.CTkImage(img, size=(self.page_width, self.page_height))
                self.pdf_images.append(label_img)
                    
                self.percentage_bar = self.percentage_bar + 1
                percentage_view = (float(self.percentage_bar) / float(len(open_pdf)) * float(100))
                self.loading_bar.set(percentage_view)
                self.percentage_load.set(f"Cargando {os.path.basename(self.file)} \n{int(math.floor(percentage_view))}%")
            
            self.loading_bar.pack_forget()
            self.loading_message.pack_forget()
            open_pdf.close()
            
            for i in self.pdf_images:
                label = customtkinter.CTkLabel(self, image=i, text="")
                label.pack(pady=(0, self.separation))
                self.labels.append(label)
        except Exception as e:
            error_message = customtkinter.CTkLabel(
                self, 
                text=f"Error al cargar el PDF:\n{str(e)}\n\nPuede abrir el archivo en:\n{os.path.abspath(self.file)}",
                justify="center",
                wraplength=400
            )
            error_message.pack(pady=20)
            
            open_button = customtkinter.CTkButton(
                self,
                text="Abrir PDF externamente",
                command=lambda: os.startfile(self.file)
            )
            open_button.pack(pady=10)
        
    def configure(self, **kwargs):
        """configurable options"""
        if "file" in kwargs:
            self.file = kwargs.pop("file")
            # Limpiar visualizador actual
            self.pdf_images = []
            for label in self.labels:
                label.destroy()
            self.labels = []
            # Reiniciar proceso de carga
            self.after(250, self.start_process)
            
        if "page_width" in kwargs:
            self.page_width = kwargs.pop("page_width")
            for img in self.pdf_images:
                img.configure(size=(self.page_width, self.page_height))
                
        if "page_height" in kwargs:
            self.page_height = kwargs.pop("page_height")
            for img in self.pdf_images:
                img.configure(size=(self.page_width, self.page_height))
            
        if "page_separation_height" in kwargs:
            self.separation = kwargs.pop("page_separation_height")
            for label in self.labels:
                label.pack_forget()
                label.pack(pady=(0, self.separation))
        
        super().configure(**kwargs)
