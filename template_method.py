"""
Módulo Template Method - Patrón de Diseño
Implementa el patrón Template Method para operaciones de validación y generación de reportes.

El patrón Template Method define el esqueleto de un algoritmo en una clase base,
dejando que las subclases implementen los pasos específicos del algoritmo.

VENTAJAS:
- Reutilización de código común
- Control sobre el flujo del algoritmo
- Evita duplicación en operaciones similares
- Fácil de extender con nuevas variantes
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from error_handler import logger, RestauranteException
from datetime import datetime
import json



# TEMPLATE METHOD 1: VALIDADOR BASE


class ValidadorTemplate(ABC):
    """
    Clase base abstracta que implementa el patrón Template Method
    para la validación de datos.
    
    Define el flujo de validación que todas las subclases deben seguir:
    1. Preparar datos
    2. Validar datos específicos
    3. Registrar resultado
    4. Retornar resultado
    """
    
    def validar(self, valor: str) -> bool:
        """
        Template Method: Define el esqueleto del algoritmo de validación
        Las subclases implementan los pasos específicos mediante métodos abstractos
        """
        try:
            # PASO 1: Preparar datos
            valor_preparado = self._preparar_datos(valor)
            logger.debug(f"Datos preparados para {self.__class__.__name__}: {valor_preparado}")
            
            # PASO 2: Validar datos específicos (implementado por subclases)
            es_valido = self._validar_especifico(valor_preparado)
            
            # PASO 3: Registrar resultado
            self._registrar_validacion(valor, es_valido)
            
            # PASO 4: Retornar resultado
            return es_valido
            
        except Exception as e:
            logger.error(f"Error en validación: {e}")
            self._registrar_validacion(valor, False, str(e))
            raise RestauranteException(f"Validación fallida: {str(e)}")
    
    def _preparar_datos(self, valor: str) -> str:
        """PASO 1: Preparación común - puede ser sobrescrito por subclases"""
        return valor.strip() if isinstance(valor, str) else str(valor)
    
    @abstractmethod
    def _validar_especifico(self, valor: str) -> bool:
        """PASO 2: Validación específica - DEBE ser implementado por subclases"""
        pass
    
    def _registrar_validacion(self, valor: str, resultado: bool, error: Optional[str] = None):
        """PASO 3: Registro de auditoría - implementado en clase base"""
        mensaje = f"Validación [{self.__class__.__name__}] - Valor: {valor}, Resultado: {resultado}"
        if error:
            mensaje += f", Error: {error}"
        logger.info(mensaje)
    
    def obtener_nombre_validador(self) -> str:
        """Hook opcional: permite personalizar el nombre del validador"""
        return self.__class__.__name__


# IMPLEMENTACIONES CONCRETAS - Validadores Específicos


class ValidadorCantidad(ValidadorTemplate):
    """
    Implementación concreta: Valida que la cantidad sea un número positivo
    Solo necesita implementar el método abstracto _validar_especifico
    """
    
    def _validar_especifico(self, valor: str) -> bool:
        """Validación específica para cantidades"""
        try:
            cantidad = float(valor)
            return cantidad > 0
        except ValueError:
            return False


class ValidadorPrecio(ValidadorTemplate):
    """
    Implementación concreta: Valida que el precio sea decimal positivo
    con máximo 2 decimales
    """
    
    def _validar_especifico(self, valor: str) -> bool:
        """Validación específica para precios"""
        try:
            precio = float(valor)
            if precio < 0:
                return False
            # Verificar máximo 2 decimales
            decimales = len(str(precio).split('.')[-1])
            return decimales <= 2
        except ValueError:
            return False


class ValidadorNombre(ValidadorTemplate):
    """
    Implementación concreta: Valida que el nombre solo contenga letras y espacios
    Sobrescribe _preparar_datos para convertir a minúsculas
    """
    
    def _preparar_datos(self, valor: str) -> str:
        """Sobrescribe preparación: convierte a minúsculas"""
        # Llama a preparación base y luego aplica lógica adicional
        valor_base = super()._preparar_datos(valor)
        return valor_base.lower()
    
    def _validar_especifico(self, valor: str) -> bool:
        """Validación específica para nombres"""
        # Solo letras y espacios
        return valor.replace(' ', '').isalpha()


class ValidadorEmail(ValidadorTemplate):
    """
    Implementación concreta: Valida formato de email básico
    """
    
    def _validar_especifico(self, valor: str) -> bool:
        """Validación específica para emails"""
        # Validación simple de email
        if '@' not in valor or '.' not in valor:
            return False
        partes = valor.split('@')
        if len(partes) != 2:
            return False
        usuario, dominio = partes
        return len(usuario) > 0 and '.' in dominio



# TEMPLATE METHOD 2: GENERADOR DE REPORTES BASE


class GeneradorReportesTemplate(ABC):
    """
    Clase base abstracta que implementa el patrón Template Method
    para la generación de diferentes tipos de reportes.
    
    Define el flujo común para cualquier tipo de reporte:
    1. Obtener datos
    2. Procesar datos
    3. Formatear reporte
    4. Guardar reporte
    """
    
    def generar_reporte(self, parametros: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Template Method: Define el esqueleto del proceso de generación
        """
        params = parametros if parametros is not None else {}
        
        try:
            logger.info(f"Iniciando generación de reporte: {self.__class__.__name__}")
            
            # PASO 1: Obtener datos
            datos_crudos = self._obtener_datos(params)
            logger.debug(f"Datos obtenidos: {len(datos_crudos)} registros")
            
            # PASO 2: Procesar datos
            datos_procesados = self._procesar_datos(datos_crudos, params)
            logger.debug(f"Datos procesados: {len(datos_procesados)} registros")
            
            # PASO 3: Formatear reporte
            reporte = self._formatear_reporte(datos_procesados, params)
            logger.debug(f"Reporte formateado: {len(reporte)} secciones")
            
            # PASO 4: Guardar reporte
            ruta_reporte = self._guardar_reporte(reporte, params)
            logger.info(f"Reporte guardado en: {ruta_reporte}")
            
            # PASO 5: Retornar resultado
            return {
                'exito': True,
                'tipo_reporte': self.__class__.__name__,
                'ruta': ruta_reporte,
                'registros_procesados': len(datos_procesados),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error al generar reporte: {e}")
            return {
                'exito': False,
                'tipo_reporte': self.__class__.__name__,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    @abstractmethod
    def _obtener_datos(self, parametros: Dict) -> List[Any]:
        """PASO 1: Obtener datos de la fuente - DEBE ser implementado por subclases"""
        pass
    
    @abstractmethod
    def _procesar_datos(self, datos: List[Any], parametros: Dict) -> List[Any]:
        """PASO 2: Procesar/transformar datos - DEBE ser implementado por subclases"""
        pass
    
    @abstractmethod
    def _formatear_reporte(self, datos: List[Any], parametros: Dict) -> Dict[str, Any]:
        """PASO 3: Formatear reporte - DEBE ser implementado por subclases"""
        pass
    
    def _guardar_reporte(self, reporte: Dict, parametros: Dict) -> str:
        """PASO 4: Guardar reporte - Implementación base (puede ser sobrescrito)"""
        # Implementación por defecto: guardar como JSON
        nombre_archivo = f"reporte_{self.__class__.__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                json.dump(reporte, f, indent=2, ensure_ascii=False)
            return nombre_archivo
        except Exception as e:
            logger.error(f"Error al guardar reporte: {e}")
            raise



# IMPLEMENTACIONES CONCRETAS - Generadores de Reportes


class ReportePedidosDiarios(GeneradorReportesTemplate):
    """
    Implementación concreta: Reporte de pedidos diarios
    Especializa el proceso de generación para pedidos
    """
    
    def _obtener_datos(self, parametros: Dict) -> List[Any]:
        """Obtiene pedidos del día actual"""
        # Aquí iría la lógica de obtener datos de BD
        # Por ahora retorna datos de ejemplo
        logger.debug("Obteniendo pedidos del día")
        return [
            {'id': 1, 'cliente': 'Juan', 'monto': 50000, 'fecha': datetime.now()},
            {'id': 2, 'cliente': 'María', 'monto': 75000, 'fecha': datetime.now()},
            {'id': 3, 'cliente': 'Pedro', 'monto': 60000, 'fecha': datetime.now()},
        ]
    
    def _procesar_datos(self, datos: List[Any], parametros: Dict) -> List[Any]:
        """Procesa pedidos: calcula totales, agrupa, etc."""
        logger.debug(f"Procesando {len(datos)} pedidos")
        
        # Ejemplo: agregar total con IVA
        for pedido in datos:
            pedido['monto_con_iva'] = pedido['monto'] * 1.19
            pedido['iva'] = pedido['monto'] * 0.19
        
        return datos
    
    def _formatear_reporte(self, datos: List[Any], parametros: Dict) -> Dict[str, Any]:
        """Formatea los datos en estructura de reporte"""
        total_monto = sum(p['monto'] for p in datos)
        total_iva = sum(p['iva'] for p in datos)
        
        return {
            'tipo': 'Reporte de Pedidos Diarios',
            'fecha': datetime.now().isoformat(),
            'cantidad_pedidos': len(datos),
            'pedidos': datos,
            'resumen': {
                'monto_total': total_monto,
                'iva_total': total_iva,
                'monto_con_iva': total_monto + total_iva,
                'promedio_pedido': total_monto / len(datos) if datos else 0
            }
        }


class ReporteProductosPopulares(GeneradorReportesTemplate):
    """
    Implementación concreta: Reporte de productos más vendidos
    Especializa el proceso para análisis de productos
    """
    
    def _obtener_datos(self, parametros: Dict) -> List[Any]:
        """Obtiene datos de ventas de productos"""
        logger.debug("Obteniendo datos de ventas de productos")
        return [
            {'producto': 'Pizza', 'cantidad': 45, 'ingresos': 225000},
            {'producto': 'Hamburguesa', 'cantidad': 67, 'ingresos': 268000},
            {'producto': 'Pasta', 'cantidad': 23, 'ingresos': 115000},
            {'producto': 'Bebida', 'cantidad': 89, 'ingresos': 89000},
        ]
    
    def _procesar_datos(self, datos: List[Any], parametros: Dict) -> List[Any]:
        """Procesa: ordena por popularidad, calcula porcentajes"""
        logger.debug(f"Procesando {len(datos)} productos")
        
        # Ordenar por cantidad vendida (descendente)
        datos_ordenados = sorted(datos, key=lambda x: x['cantidad'], reverse=True)
        
        # Calcular porcentajes
        total_cantidad = sum(p['cantidad'] for p in datos_ordenados)
        for producto in datos_ordenados:
            producto['porcentaje'] = (producto['cantidad'] / total_cantidad * 100) if total_cantidad > 0 else 0
        
        return datos_ordenados
    
    def _formatear_reporte(self, datos: List[Any], parametros: Dict) -> Dict[str, Any]:
        """Formatea reporte de productos populares"""
        total_ingresos = sum(p['ingresos'] for p in datos)
        
        return {
            'tipo': 'Reporte de Productos Populares',
            'fecha': datetime.now().isoformat(),
            'total_productos': len(datos),
            'productos': datos,
            'ranking': [
                {
                    'posicion': i + 1,
                    'producto': p['producto'],
                    'cantidad': p['cantidad'],
                    'porcentaje': round(p['porcentaje'], 2)
                }
                for i, p in enumerate(datos[:5])  # Top 5
            ],
            'resumen': {
                'total_vendido': sum(p['cantidad'] for p in datos),
                'ingresos_totales': total_ingresos,
                'producto_mas_vendido': datos[0]['producto'] if datos else 'N/A',
                'cantidad_mas_vendida': datos[0]['cantidad'] if datos else 0
            }
        }


class ReporteClientesLeales(GeneradorReportesTemplate):
    """
    Implementación concreta: Reporte de clientes más leales
    Especializa el proceso para análisis de clientes
    """
    
    def _obtener_datos(self, parametros: Dict) -> List[Any]:
        """Obtiene datos de clientes"""
        logger.debug("Obteniendo datos de clientes")
        return [
            {'cliente': 'Juan García', 'pedidos': 12, 'monto_total': 450000},
            {'cliente': 'María López', 'pedidos': 8, 'monto_total': 380000},
            {'cliente': 'Pedro Sánchez', 'pedidos': 15, 'monto_total': 620000},
            {'cliente': 'Ana Martínez', 'pedidos': 5, 'monto_total': 180000},
        ]
    
    def _procesar_datos(self, datos: List[Any], parametros: Dict) -> List[Any]:
        """Procesa: ordena por lealtad (cantidad de pedidos)"""
        logger.debug(f"Procesando {len(datos)} clientes")
        
        # Ordenar por cantidad de pedidos (descendente)
        datos_ordenados = sorted(datos, key=lambda x: x['pedidos'], reverse=True)
        
        # Calcular ticket promedio
        for cliente in datos_ordenados:
            cliente['ticket_promedio'] = cliente['monto_total'] / cliente['pedidos'] if cliente['pedidos'] > 0 else 0
        
        return datos_ordenados
    
    def _formatear_reporte(self, datos: List[Any], parametros: Dict) -> Dict[str, Any]:
        """Formatea reporte de clientes leales"""
        return {
            'tipo': 'Reporte de Clientes Leales',
            'fecha': datetime.now().isoformat(),
            'total_clientes': len(datos),
            'clientes': datos,
            'top_clientes': [
                {
                    'posicion': i + 1,
                    'cliente': c['cliente'],
                    'pedidos': c['pedidos'],
                    'monto_total': c['monto_total'],
                    'ticket_promedio': round(c['ticket_promedio'], 2)
                }
                for i, c in enumerate(datos[:3])  # Top 3
            ],
            'resumen': {
                'clientes_activos': len(datos),
                'pedidos_totales': sum(c['pedidos'] for c in datos),
                'ingresos_totales': sum(c['monto_total'] for c in datos),
                'ticket_promedio_general': round(sum(c['monto_total'] for c in datos) / max(sum(c['pedidos'] for c in datos), 1), 2)
            }
        }



# EJEMPLO DE USO Y PRUEBAS


if __name__ == "__main__":
    """
    Ejemplos de uso del patrón Template Method
    """
    
    logger.info("=" * 80)
    logger.info("DEMOSTRACION DEL PATRON TEMPLATE METHOD")
    logger.info("=" * 80)
    
    # ===== EJEMPLO 1: VALIDADORES =====
    logger.info("\n1. VALIDADORES (Template Method para Validación)")
    logger.info("-" * 80)
    
    validadores = [
        ValidadorCantidad(),
        ValidadorPrecio(),
        ValidadorNombre(),
        ValidadorEmail()
    ]
    
    casos_prueba = [
        ("100", "cantidad"),
        ("-50", "cantidad"),
        ("99.99", "precio"),
        ("100.999", "precio"),
        ("juan perez", "nombre"),
        ("juan123", "nombre"),
        ("juan@email.com", "email"),
        ("email_invalido", "email")
    ]
    
    for valor, tipo_esperado in casos_prueba:
        for validador in validadores:
            if validador.__class__.__name__.lower().replace("validador", "") in tipo_esperado.lower():
                try:
                    resultado = validador.validar(valor)
                    print(f"✓ {validador.__class__.__name__}('{valor}') = {resultado}")
                except Exception as e:
                    print(f"✗ {validador.__class__.__name__}('{valor}') = Error: {e}")
    
    # ===== EJEMPLO 2: GENERADORES DE REPORTES =====
    logger.info("\n2. GENERADORES DE REPORTES (Template Method para Reportes)")
    logger.info("-" * 80)
    
    generadores = [
        ReportePedidosDiarios(),
        ReporteProductosPopulares(),
        ReporteClientesLeales()
    ]
    
    for generador in generadores:
        logger.info(f"\nGenerando {generador.__class__.__name__}...")
        resultado = generador.generar_reporte()
        
        if resultado['exito']:
            print(f"\n✓ {generador.__class__.__name__}")
            print(f"  - Archivo: {resultado['ruta']}")
            print(f"  - Registros procesados: {resultado['registros_procesados']}")
            print(f"  - Timestamp: {resultado['timestamp']}")
        else:
            print(f"\n✗ {generador.__class__.__name__}")
            print(f"  - Error: {resultado['error']}")
    
    logger.info("\n" + "=" * 80)
    logger.info("FIN DE LA DEMOSTRACION")
    logger.info("=" * 80)
