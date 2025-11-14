"""
Módulo de utilidades para la aplicación de gestión de restaurante.

Proporciona funciones auxiliares reutilizables para:
- Validación de datos
- Formateo de valores monetarios
- Cálculo de totales
- Operaciones con archivos
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import List, Dict
import os


class UtilFormatter:
    """Utilidades para formateo de datos en la interfaz"""
    
    @staticmethod
    def formatear_precio(precio: float) -> str:
        """
        Formatea un precio para mostrar en la interfaz.
        
        Args:
            precio (float): Precio a formatear
            
        Returns:
            str: Precio formateado con 2 decimales y símbolo $
            
        Ejemplo:
            >>> UtilFormatter.formatear_precio(1500.5)
            '$1.500,50'
        """
        try:
            # Convertir a Decimal para precisión
            d = Decimal(str(precio)).quantize(
                Decimal('0.01'),
                rounding=ROUND_HALF_UP
            )
            # Formatear con separadores
            return f"${d:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except (ValueError, TypeError):
            return "$0,00"
    
    @staticmethod
    def formatear_cantidad(cantidad: float, decimales: int = 2) -> str:
        """
        Formatea una cantidad con el número especificado de decimales.
        
        Args:
            cantidad (float): Cantidad a formatear
            decimales (int): Número de decimales (por defecto 2)
            
        Returns:
            str: Cantidad formateada
            
        Ejemplo:
            >>> UtilFormatter.formatear_cantidad(10.5)
            '10.50'
        """
        try:
            return f"{float(cantidad):.{decimales}f}"
        except (ValueError, TypeError):
            return f"{0:.{decimales}f}"
    
    @staticmethod
    def obtener_extension(ruta: str) -> str:
        """
        Obtiene la extensión de un archivo.
        
        Args:
            ruta (str): Ruta del archivo
            
        Returns:
            str: Extensión en minúsculas (sin punto)
            
        Ejemplo:
            >>> UtilFormatter.obtener_extension("datos.csv")
            'csv'
        """
        if not ruta:
            return ""
        return os.path.splitext(ruta)[1].lower().lstrip('.')


class UtilCalculos:
    """Utilidades para cálculos matemáticos comunes"""
    
    @staticmethod
    def calcular_total_pedido(items: List[Dict]) -> Decimal:
        """
        Calcula el total de un pedido sumando los precios de items.
        
        Args:
            items (List[Dict]): Lista de items con estructura:
                [{
                    'precio': float,
                    'cantidad': int,
                    'descuento': float (opcional, por defecto 0)
                }, ...]
                
        Returns:
            Decimal: Total del pedido con precisión monetaria
            
        Raises:
            ValueError: Si los items no tienen estructura válida
            
        Ejemplo:
            >>> items = [
            ...     {'precio': 100, 'cantidad': 2},
            ...     {'precio': 50, 'cantidad': 1, 'descuento': 10}
            ... ]
            >>> UtilCalculos.calcular_total_pedido(items)
            Decimal('240.00')
        """
        total = Decimal('0')
        
        for item in items:
            try:
                precio = Decimal(str(item.get('precio', 0)))
                cantidad = Decimal(str(item.get('cantidad', 1)))
                descuento = Decimal(str(item.get('descuento', 0)))
                
                subtotal = precio * cantidad
                descuento_monto = (subtotal * descuento) / Decimal('100')
                
                total += subtotal - descuento_monto
            except (ValueError, TypeError, KeyError) as e:
                raise ValueError(f"Item inválido en pedido: {e}")
        
        return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def aplicar_descuento(monto: float, porcentaje_descuento: float) -> Decimal:
        """
        Calcula el monto después de aplicar un descuento.
        
        Args:
            monto (float): Monto original
            porcentaje_descuento (float): Porcentaje de descuento (0-100)
            
        Returns:
            Decimal: Monto con descuento aplicado
            
        Ejemplo:
            >>> UtilCalculos.aplicar_descuento(1000, 10)
            Decimal('900.00')
        """
        monto_d = Decimal(str(monto))
        desc_d = Decimal(str(porcentaje_descuento))
        
        if desc_d < 0 or desc_d > 100:
            raise ValueError("El descuento debe estar entre 0 y 100")
        
        descuento = (monto_d * desc_d) / Decimal('100')
        resultado = monto_d - descuento
        
        return resultado.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


class UtilArchivos:
    """Utilidades para manejo de archivos"""
    
    @staticmethod
    def existe_archivo(ruta: str) -> bool:
        """
        Verifica si un archivo existe en la ruta especificada.
        
        Args:
            ruta (str): Ruta del archivo
            
        Returns:
            bool: True si existe, False en caso contrario
            
        Ejemplo:
            >>> UtilArchivos.existe_archivo("datos.csv")
            True
        """
        return os.path.isfile(ruta) if ruta else False
    
    @staticmethod
    def obtener_nombre_archivo(ruta: str) -> str:
        """
        Extrae el nombre del archivo de una ruta completa.
        
        Args:
            ruta (str): Ruta completa del archivo
            
        Returns:
            str: Nombre del archivo con extensión
            
        Ejemplo:
            >>> UtilArchivos.obtener_nombre_archivo("/home/user/archivo.pdf")
            'archivo.pdf'
        """
        return os.path.basename(ruta) if ruta else ""
    
    @staticmethod
    def crear_directorio_si_no_existe(ruta_dir: str) -> bool:
        """
        Crea un directorio si no existe.
        
        Args:
            ruta_dir (str): Ruta del directorio a crear
            
        Returns:
            bool: True si se creó o ya existía, False si hay error
            
        Ejemplo:
            >>> UtilArchivos.crear_directorio_si_no_existe("./reportes")
            True
        """
        try:
            if not os.path.exists(ruta_dir):
                os.makedirs(ruta_dir, exist_ok=True)
            return True
        except OSError:
            return False


class UtilValidacion:
    """Utilidades para validación de datos de entrada"""
    
    @staticmethod
    def es_numero(valor: str) -> bool:
        """
        Verifica si un string es un número válido.
        
        Args:
            valor (str): String a validar
            
        Returns:
            bool: True si es número, False en caso contrario
            
        Ejemplo:
            >>> UtilValidacion.es_numero("123.45")
            True
            >>> UtilValidacion.es_numero("abc")
            False
        """
        try:
            float(valor)
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def es_positivo(valor: float) -> bool:
        """
        Verifica si un número es positivo (mayor a 0).
        
        Args:
            valor (float): Número a validar
            
        Returns:
            bool: True si es positivo
            
        Ejemplo:
            >>> UtilValidacion.es_positivo(10.5)
            True
            >>> UtilValidacion.es_positivo(-5)
            False
        """
        try:
            return float(valor) > 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def longitud_valida(texto: str, min_len: int = 1, max_len: int = 255) -> bool:
        """
        Verifica si la longitud de un texto está dentro del rango especificado.
        
        Args:
            texto (str): Texto a validar
            min_len (int): Longitud mínima (por defecto 1)
            max_len (int): Longitud máxima (por defecto 255)
            
        Returns:
            bool: True si la longitud es válida
            
        Ejemplo:
            >>> UtilValidacion.longitud_valida("Hamburguesa", 3, 20)
            True
        """
        if not isinstance(texto, str):
            return False
        longitud = len(texto.strip())
        return min_len <= longitud <= max_len
