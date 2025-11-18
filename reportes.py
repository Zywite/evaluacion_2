# -*- coding: utf-8 -*-
"""
Módulo: Generador de Reportes Integrado
Proporciona funcionalidad para generar reportes en múltiples formatos.

Integra el patrón Template Method para especializar la generación de reportes
según el formato requerido (JSON, CSV, HTML).

Uso:
    from reportes import ReporteJSON, ReporteCSV, ReporteHTML
    
    # Generar reporte de pedidos
    reporte_json = ReporteJSON()
    archivo = reporte_json.generar("pedidos")
"""

import json
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

from error_handler import logger, RestauranteException
from database import get_db_session
from models import Pedido
from sqlalchemy.orm import Session


# Crear directorio de reportes si no existe
REPORTES_DIR = Path("reportes")
REPORTES_DIR.mkdir(exist_ok=True)


class GeneradorReporteTemplate(ABC):
    """
    Clase base para generadores de reportes.
    Implementa el patrón Template Method para la generación de reportes.
    
    Flujo estándar:
    1. Obtener datos de la base de datos
    2. Procesar/transformar datos
    3. Formatear estructura del reporte
    4. Guardar archivo
    5. Retornar ruta del archivo
    """
    
    def generar(self, tipo_reporte: str, db: Optional[Session] = None) -> str:
        """
        Template Method: Define el flujo completo de generación de reportes.
        Las subclases especializan los pasos específicos.
        """
        try:
            logger.info(f"Iniciando generación de reporte: {tipo_reporte}")
            
            # PASO 1: Obtener datos
            datos = self._obtener_datos(tipo_reporte, db)
            logger.debug(f"Datos obtenidos: {len(datos)} registros")
            
            # PASO 2: Procesar datos
            datos_procesados = self._procesar_datos(datos)
            logger.debug("Datos procesados correctamente")
            
            # PASO 3: Formatear reporte
            contenido_formateado = self._formatear_contenido(datos_procesados)
            logger.debug("Contenido formateado")
            
            # PASO 4: Guardar archivo
            archivo_path = self._guardar_archivo(contenido_formateado, tipo_reporte)
            logger.info(f"Reporte guardado en: {archivo_path}")
            
            return archivo_path
            
        except Exception as e:
            logger.error(f"Error generando reporte: {str(e)}", exc_info=True)
            raise RestauranteException(f"Error al generar reporte: {str(e)}")
    
    @abstractmethod
    def _obtener_datos(self, tipo_reporte: str, db: Optional[Session]) -> List[Dict]:
        """Paso 1: Obtener datos de BD - implementar en subclases"""
        pass
    
    def _procesar_datos(self, datos: List[Dict]) -> List[Dict]:
        """Paso 2: Procesar datos - puede ser override"""
        return datos
    
    @abstractmethod
    def _formatear_contenido(self, datos: List[Dict]) -> str:
        """Paso 3: Formatear contenido - implementar en subclases"""
        pass
    
    @abstractmethod
    def _guardar_archivo(self, contenido: str, tipo_reporte: str) -> str:
        """Paso 4: Guardar archivo - implementar en subclases"""
        pass
    
    def _obtener_datos_pedidos(self, db: Optional[Session]) -> List[Dict]:
        """Obtiene todos los pedidos de la BD"""
        if db is None:
            db = get_db_session()
        
        pedidos = db.query(Pedido).all()
        datos = []
        
        for pedido in pedidos:
            datos.append({
                'id': pedido.id,
                'cliente_id': pedido.cliente_id,
                'cliente_nombre': pedido.cliente.nombre if pedido.cliente else 'N/A',
                'fecha': pedido.fecha.isoformat() if pedido.fecha else '',
                'total': float(pedido.total) if pedido.total else 0,
                'estado': pedido.estado,
                'cantidad_items': len(pedido.items)
            })
        
        return datos


class ReporteJSON(GeneradorReporteTemplate):
    """Generador de reportes en formato JSON"""
    
    def _obtener_datos(self, tipo_reporte: str, db: Optional[Session]) -> List[Dict]:
        """Obtiene datos según tipo de reporte"""
        if tipo_reporte == "pedidos":
            return self._obtener_datos_pedidos(db)
        else:
            raise RestauranteException(f"Tipo de reporte no soportado: {tipo_reporte}")
    
    def _formatear_contenido(self, datos: List[Dict]) -> str:
        """Formatea datos como JSON"""
        reporte = {
            'tipo': 'Reporte JSON',
            'fecha_generacion': datetime.now().isoformat(),
            'cantidad_registros': len(datos),
            'datos': datos,
            'resumen': {
                'total_pedidos': len(datos),
                'monto_total': sum(d['total'] for d in datos),
                'promedio': sum(d['total'] for d in datos) / len(datos) if datos else 0
            }
        }
        
        return json.dumps(reporte, indent=2, ensure_ascii=False, default=str)
    
    def _guardar_archivo(self, contenido: str, tipo_reporte: str) -> str:
        """Guarda contenido en archivo JSON"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        archivo_name = f"{tipo_reporte}_{timestamp}.json"
        archivo_path = REPORTES_DIR / archivo_name
        
        with open(archivo_path, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        return str(archivo_path)


class ReporteCSV(GeneradorReporteTemplate):
    """Generador de reportes en formato CSV"""
    
    def _obtener_datos(self, tipo_reporte: str, db: Optional[Session]) -> List[Dict]:
        """Obtiene datos según tipo de reporte"""
        if tipo_reporte == "pedidos":
            return self._obtener_datos_pedidos(db)
        else:
            raise RestauranteException(f"Tipo de reporte no soportado: {tipo_reporte}")
    
    def _formatear_contenido(self, datos: List[Dict]) -> str:
        """Formatea datos como CSV"""
        if not datos:
            return ""
        
        # Obtener headers del primer registro
        headers = list(datos[0].keys())
        
        # Crear contenido CSV
        lineas = [','.join(headers)]
        
        for fila in datos:
            valores = [
                str(fila.get(header, '')).replace(',', ';')
                for header in headers
            ]
            lineas.append(','.join(valores))
        
        return '\n'.join(lineas)
    
    def _guardar_archivo(self, contenido: str, tipo_reporte: str) -> str:
        """Guarda contenido en archivo CSV"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        archivo_name = f"{tipo_reporte}_{timestamp}.csv"
        archivo_path = REPORTES_DIR / archivo_name
        
        with open(archivo_path, 'w', encoding='utf-8', newline='') as f:
            f.write(contenido)
        
        return str(archivo_path)


class ReporteHTML(GeneradorReporteTemplate):
    """Generador de reportes en formato HTML"""
    
    def _obtener_datos(self, tipo_reporte: str, db: Optional[Session]) -> List[Dict]:
        """Obtiene datos según tipo de reporte"""
        if tipo_reporte == "pedidos":
            return self._obtener_datos_pedidos(db)
        else:
            raise RestauranteException(f"Tipo de reporte no soportado: {tipo_reporte}")
    
    def _formatear_contenido(self, datos: List[Dict]) -> str:
        """Formatea datos como HTML"""
        if not datos:
            headers = ""
            filas = ""
        else:
            # Headers
            headers_list = list(datos[0].keys())
            headers = '\n'.join([f"<th>{h}</th>" for h in headers_list])
            
            # Filas
            filas_list = []
            for dato in datos:
                fila = '\n'.join([f"<td>{dato.get(h, '')}</td>" for h in headers_list])
                filas_list.append(f"<tr>\n{fila}\n</tr>")
            filas = '\n'.join(filas_list)
        
        # Usar f-string para evitar conflictos con llaves del CSS
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reporte</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #4CAF50; color: white; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                .header {{ color: #333; margin-bottom: 20px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Reporte de Pedidos</h1>
                <p>Generado: {fecha}</p>
            </div>
            <table>
                <thead>
                    <tr>
                        {headers}
                    </tr>
                </thead>
                <tbody>
                    {filas}
                </tbody>
            </table>
        </body>
        </html>
        """
        return html
    
    def _guardar_archivo(self, contenido: str, tipo_reporte: str) -> str:
        """Guarda contenido en archivo HTML"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        archivo_name = f"{tipo_reporte}_{timestamp}.html"
        archivo_path = REPORTES_DIR / archivo_name
        
        with open(archivo_path, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        return str(archivo_path)


# Función de conveniencia
def generar_reporte(formato: str = "json", tipo: str = "pedidos", db: Optional[Session] = None) -> str:
    """
    Función de conveniencia para generar reportes.
    
    Args:
        formato: 'json', 'csv', 'html'
        tipo: 'pedidos', etc.
        db: Sesión de BD (opcional)
    
    Returns:
        Ruta del archivo generado
    
    Ejemplo:
        archivo = generar_reporte("json", "pedidos")
        archivo = generar_reporte("csv", "pedidos")
        archivo = generar_reporte("html", "pedidos")
    """
    generadores = {
        'json': ReporteJSON,
        'csv': ReporteCSV,
        'html': ReporteHTML,
    }
    
    if formato not in generadores:
        raise RestauranteException(f"Formato no soportado: {formato}")
    
    generador = generadores[formato]()
    return generador.generar(tipo, db)
