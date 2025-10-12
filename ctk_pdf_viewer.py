
from typing import Union
import customtkinter
from customtkinter import CTk, CTkFrame
from PIL import Image
import fitz
from threading import Thread
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

        self._page_width = page_width
        self._page_height = page_height
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
            with fitz.open(self.file) as open_pdf:
                num_pages = len(open_pdf)
                
                for page_num in range(num_pages):
                    page = open_pdf[page_num]
                    pix = page.get_pixmap(alpha=False)  # type: ignore
                    img = Image.open(io.BytesIO(pix.tobytes('ppm')))
                    
                    # Usamos after para asegurar que la UI se actualice en el hilo principal
                    self.after(0, self._update_page, img, page_num, num_pages)

                self.after(100, self._finalize_loading)

        except Exception as e:
            self.after(0, self._display_error, e)

    def _update_page(self, img: Image.Image, page_num: int, total_pages: int):
        """Crea y muestra una página del PDF. Se ejecuta en el hilo principal."""
        ctk_img = customtkinter.CTkImage(img, size=(self._page_width, self._page_height))
        self.pdf_images.append(ctk_img)

        label = customtkinter.CTkLabel(self, image=ctk_img, text="")
        label.pack(pady=(0, self.separation))
        self.labels.append(label)

        progress = (page_num + 1) / total_pages
        self.loading_bar.set(progress)
        self.percentage_load.set(f"Cargando {os.path.basename(self.file)} \n{int(progress * 100)}%")

    def _finalize_loading(self):
        """Oculta los widgets de carga. Se ejecuta en el hilo principal."""
        self.loading_bar.pack_forget()
        self.loading_message.pack_forget()

    def _display_error(self, e: Exception):
        """Muestra un mensaje de error. Se ejecuta en el hilo principal."""
        self.loading_bar.pack_forget()
        self.loading_message.pack_forget()
        error_message = customtkinter.CTkLabel(
            self, 
            text=f"Error al cargar el PDF:\n{e}\n\nPuede abrir el archivo en:\n{os.path.abspath(self.file)}",
            justify="center",
            wraplength=self.winfo_width() - 40
        )
        error_message.pack(pady=20, padx=20, fill="x")
        
        open_button = customtkinter.CTkButton(self, text="Abrir PDF externamente", command=lambda: os.startfile(self.file))
        open_button.pack(pady=10)
        
    def configure(self, **kwargs):
        """configurable options"""
        if "file" in kwargs:
            self.file = kwargs.pop("file")
            # Limpiar completamente el visualizador actual
            for label in self.labels:
                if label.winfo_exists():
                    label.destroy()
            self.labels.clear()
            self.pdf_images = []
            
            # Reiniciar proceso de carga
            self.loading_message.pack(pady=10)
            self.loading_bar.pack(side="top", fill="x", padx=10)
            self.loading_bar.set(0)
            self.percentage_load.set("")
            self.after(250, self.start_process)
            
        if "page_width" in kwargs:
            self._page_width = kwargs.pop("page_width")
            for img in self.pdf_images:
                img.configure(size=(self._page_width, self._page_height))
                
        if "page_height" in kwargs:
            self._page_height = kwargs.pop("page_height")
            for img in self.pdf_images:
                img.configure(size=(self._page_width, self._page_height))
            
        if "page_separation_height" in kwargs:
            self.separation = kwargs.pop("page_separation_height")
            for label in self.labels:
                label.pack_forget()
                label.pack(pady=(0, self.separation))
        
        super().configure(**kwargs)
