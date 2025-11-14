"""
Módulo de manejo centralizado de errores y logging
Proporciona validación, logging y mensajes de error consistentes
"""

import logging
import sys
from typing import Callable, Any


# Configurar logging
class LoggerConfig:
    """Configuración centralizada de logging"""
    
    _logger = None
    
    @classmethod
    def get_logger(cls, name: str = "RestauranteApp") -> logging.Logger:
        """Obtiene o crea el logger configurado"""
        if cls._logger is None:
            cls._logger = logging.getLogger(name)
            cls._logger.setLevel(logging.DEBUG)
            
            # Handler para archivo
            file_handler = logging.FileHandler('restaurante.log')
            file_handler.setLevel(logging.DEBUG)
            
            # Handler para consola
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            
            # Formato
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            cls._logger.addHandler(file_handler)
            cls._logger.addHandler(console_handler)
        
        return cls._logger


logger = LoggerConfig.get_logger()


# Excepciones personalizadas
class RestauranteException(Exception):
    """Excepción base para la aplicación"""
    pass


class StockException(RestauranteException):
    """Excepción relacionada con stock/inventario"""
    pass


class PedidoException(RestauranteException):
    """Excepción relacionada con pedidos"""
    pass


class CSVException(RestauranteException):
    """Excepción relacionada con carga de CSV"""
    pass


class BolletaException(RestauranteException):
    """Excepción relacionada con generación de boletas"""
    pass


# Funciones de validación
class Validador:
    """Clase con métodos de validación reutilizables"""
    
    @staticmethod
    def validar_cantidad(cantidad: Any, nombre_campo: str = "cantidad") -> float:
        """
        Valida que cantidad sea un número positivo
        
        Args:
            cantidad: Valor a validar
            nombre_campo: Nombre del campo para el mensaje
            
        Returns:
            float: Cantidad validada
            
        Raises:
            ValueError: Si la cantidad es inválida
        """
        try:
            cant = float(cantidad)
            if cant <= 0:
                raise ValueError(f"{nombre_campo} debe ser mayor a 0")
            return cant
        except (ValueError, TypeError) as e:
            logger.error(f"Error validando {nombre_campo}: {e}")
            raise ValueError(f"{nombre_campo} debe ser un número válido")
    
    @staticmethod
    def validar_precio(precio: Any) -> float:
        """Valida que precio sea un número positivo"""
        try:
            p = float(precio)
            if p < 0:
                raise ValueError("El precio no puede ser negativo")
            return p
        except (ValueError, TypeError) as e:
            logger.error(f"Error validando precio: {e}")
            raise ValueError("El precio debe ser un número válido")
    
    @staticmethod
    def validar_string(valor: Any, longitud_min: int = 1, 
                      nombre_campo: str = "campo") -> str:
        """Valida que valor sea un string válido"""
        if not isinstance(valor, str) or len(valor.strip()) < longitud_min:
            raise ValueError(
                f"{nombre_campo} debe tener al menos {longitud_min} caracteres"
            )
        return valor.strip()
    
    @staticmethod
    def validar_archivo_csv(ruta: str) -> str:
        """Valida que la ruta sea un archivo CSV válido"""
        if not isinstance(ruta, str) or not ruta.endswith('.csv'):
            raise CSVException("El archivo debe ser un CSV válido")
        
        import os
        if not os.path.exists(ruta):
            raise CSVException(f"El archivo no existe: {ruta}")
        
        return ruta


# Decorador para manejo automático de errores
def manejo_errores(func: Callable) -> Callable:
    """
    Decorador que captura excepciones y las registra
    
    Args:
        func: Función a decorar
        
    Returns:
        Función decorada con manejo de errores
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RestauranteException as e:
            logger.error(f"Error en {func.__name__}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado en {func.__name__}: {e}", exc_info=True)
            raise RestauranteException(
                f"Error inesperado: {str(e)[:100]}"
            )
    
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


# Mensajes de error amigables
class MensajesError:
    """Mensajes de error consistentes para la UI"""
    
    STOCK_INSUFICIENTE = (
        "Stock insuficiente",
        "No hay suficientes ingredientes disponibles para este producto."
    )
    
    CSV_INVALIDO = (
        "Archivo inválido",
        "El archivo CSV no tiene el formato correcto. "
        "Verifique que incluya: nombre, cantidad, precio."
    )
    
    PEDIDO_VACIO = (
        "Pedido vacío",
        "Debe agregar al menos un producto antes de generar la boleta."
    )
    
    ERROR_GENERANDO_BOLETA = (
        "Error en boleta",
        "No se pudo generar la boleta. Intente nuevamente."
    )
    
    CAMPO_REQUERIDO = (
        "Campo requerido",
        "Debe completar todos los campos obligatorios."
    )
    
    PRECIO_INVALIDO = (
        "Precio inválido",
        "El precio debe ser un número positivo válido."
    )
    
    CANTIDAD_INVALIDA = (
        "Cantidad inválida",
        "La cantidad debe ser un número positivo válido."
    )
    
    @staticmethod
    def get_mensaje(tipo: tuple) -> tuple:
        """Retorna tupla (titulo, mensaje)"""
        return tipo
