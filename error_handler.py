"""
Módulo de manejo centralizado de errores y logging
Proporciona validación, logging y mensajes de error consistentes

Integra el patrón Template Method para validaciones reutilizables,
permitiendo extender fácilmente con nuevos tipos de validadores.
"""

import logging
import sys
from typing import Callable, Any
from abc import ABC, abstractmethod


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


# ============================================================================
# TEMPLATE METHOD - VALIDADORES ESPECIALIZADOS
# ============================================================================

class ValidadorTemplate(ABC):
    """
    Clase base abstracta que implementa el patrón Template Method
    para validación de datos específicos.
    
    El patrón define el flujo común de validación:
    1. Preparar datos (trim, conversión, etc.)
    2. Aplicar validación específica
    3. Registrar resultado en logs
    4. Retornar resultado
    
    Esto permite extender con nuevos validadores sin duplicar código.
    """
    
    def validar(self, valor: str) -> bool:
        """
        Template Method: Define el esqueleto del algoritmo de validación
        Las subclases implementan los pasos específicos
        """
        try:
            # PASO 1: Preparar datos (implementado por subclases)
            valor_preparado = self._preparar_datos(valor)
            logger.debug(f"Datos preparados para {self.__class__.__name__}: {valor_preparado}")
            
            # PASO 2: Validar datos específicos (implementado por subclases)
            es_valido = self._validar_especifico(valor_preparado)
            
            # PASO 3: Registrar validación
            self._registrar_validacion(valor_preparado, es_valido)
            
            return es_valido
        except Exception as e:
            logger.error(f"Error en validación {self.__class__.__name__}: {e}")
            self._registrar_validacion(valor, False)
            return False
    
    def _preparar_datos(self, valor: str) -> str:
        """Hook: Preparación de datos (puede ser override por subclases)"""
        return str(valor).strip()
    
    @abstractmethod
    def _validar_especifico(self, valor: str) -> bool:
        """Método abstracto: Validación específica a implementar por subclases"""
        pass
    
    def _registrar_validacion(self, valor: str, resultado: bool) -> None:
        """Hook: Registro de validación (puede ser override por subclases)"""
        estado = "válido" if resultado else "inválido"
        logger.info(f"{self.__class__.__name__}: '{valor}' - {estado}")


class ValidadorCantidad(ValidadorTemplate):
    """Validador especializado para cantidades numéricas positivas"""
    
    def _validar_especifico(self, valor: str) -> bool:
        """Valida que sea un número positivo"""
        try:
            cant = float(valor)
            return cant > 0
        except (ValueError, TypeError):
            return False


class ValidadorPrecio(ValidadorTemplate):
    """Validador especializado para precios (no negativos)"""
    
    def _validar_especifico(self, valor: str) -> bool:
        """Valida que sea un número no negativo"""
        try:
            precio = float(valor)
            return precio >= 0
        except (ValueError, TypeError):
            return False


class ValidadorNombre(ValidadorTemplate):
    """Validador especializado para nombres/strings"""
    
    def __init__(self, longitud_minima: int = 2):
        self.longitud_minima = longitud_minima
    
    def _validar_especifico(self, valor: str) -> bool:
        """Valida que tenga longitud mínima y caracteres válidos"""
        return len(valor) >= self.longitud_minima and valor.replace(" ", "").isalnum()


class ValidadorEmail(ValidadorTemplate):
    """Validador especializado para emails"""
    
    def _validar_especifico(self, valor: str) -> bool:
        """Valida formato básico de email"""
        return "@" in valor and "." in valor.split("@")[-1] if "@" in valor else False


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
