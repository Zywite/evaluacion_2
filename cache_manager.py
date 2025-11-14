"""
Módulo de caché para optimizar operaciones frecuentes.

Implementa un sistema de caché con TTL (Time To Live)
para mejorar el performance de búsquedas repetidas.
"""

import time
from typing import Any, Callable, Optional, Dict
from functools import wraps
import threading


class CacheItem:
    """Representa un item en caché con información de expiración"""
    
    def __init__(self, valor: Any, ttl: Optional[int] = None):
        """
        Inicializa un item de caché.
        
        Args:
            valor: Valor a cachear
            ttl: Tiempo de vida en segundos (None = sin expiración)
        """
        self.valor = valor
        self.timestamp = time.time()
        self.ttl = ttl
    
    def esta_expirado(self) -> bool:
        """Verifica si el item ha expirado"""
        if self.ttl is None:
            return False
        tiempo_transcurrido = time.time() - self.timestamp
        return tiempo_transcurrido > self.ttl


class Cache:
    """
    Implementación de un caché simple con TTL.
    Thread-safe para uso en aplicaciones multihilo.
    """
    
    def __init__(self, ttl_default: int = 300):
        """
        Inicializa el caché.
        
        Args:
            ttl_default: TTL por defecto en segundos (300 = 5 minutos)
        """
        self._datos: Dict[str, CacheItem] = {}
        self._lock = threading.Lock()
        self.ttl_default = ttl_default
        self._estadisticas = {
            'hits': 0,
            'misses': 0,
            'escrituras': 0
        }
    
    def set(self, clave: str, valor: Any, ttl: Optional[int] = None) -> None:
        """
        Almacena un valor en caché.
        
        Args:
            clave: Identificador único del valor
            valor: Valor a almacenar
            ttl: Tiempo de vida (None usa el default)
            
        Ejemplo:
            >>> cache = Cache()
            >>> cache.set('usuario_1', {'nombre': 'Juan'}, ttl=600)
        """
        ttl_final = ttl if ttl is not None else self.ttl_default
        
        with self._lock:
            self._datos[clave] = CacheItem(valor, ttl_final)
            self._estadisticas['escrituras'] += 1
    
    def get(self, clave: str, default: Any = None) -> Any:
        """
        Obtiene un valor del caché.
        
        Args:
            clave: Identificador del valor
            default: Valor por defecto si no existe o ha expirado
            
        Returns:
            El valor cacheado o el default
            
        Ejemplo:
            >>> cache.get('usuario_1')
            {'nombre': 'Juan'}
        """
        with self._lock:
            if clave not in self._datos:
                self._estadisticas['misses'] += 1
                return default
            
            item = self._datos[clave]
            
            if item.esta_expirado():
                del self._datos[clave]
                self._estadisticas['misses'] += 1
                return default
            
            self._estadisticas['hits'] += 1
            return item.valor
    
    def existe(self, clave: str) -> bool:
        """Verifica si una clave existe y no está expirada"""
        with self._lock:
            if clave not in self._datos:
                return False
            
            item = self._datos[clave]
            if item.esta_expirado():
                del self._datos[clave]
                return False
            
            return True
    
    def eliminar(self, clave: str) -> None:
        """Elimina un valor del caché"""
        with self._lock:
            if clave in self._datos:
                del self._datos[clave]
    
    def limpiar(self) -> None:
        """Limpia todo el caché"""
        with self._lock:
            self._datos.clear()
            self._estadisticas = {'hits': 0, 'misses': 0, 'escrituras': 0}
    
    def limpiar_expirados(self) -> int:
        """
        Elimina todos los items expirados.
        
        Returns:
            Número de items eliminados
        """
        with self._lock:
            claves_expiradas = [
                clave for clave, item in self._datos.items()
                if item.esta_expirado()
            ]
            
            for clave in claves_expiradas:
                del self._datos[clave]
            
            return len(claves_expiradas)
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """
        Retorna estadísticas de uso del caché.
        
        Returns:
            Dict con hits, misses, escrituras y tasa de acierto
            
        Ejemplo:
            >>> cache.obtener_estadisticas()
            {
                'hits': 42,
                'misses': 8,
                'escrituras': 15,
                'tasa_acierto': 0.84
            }
        """
        with self._lock:
            total = self._estadisticas['hits'] + self._estadisticas['misses']
            tasa_acierto = (
                self._estadisticas['hits'] / total
                if total > 0 else 0
            )
            
            return {
                'hits': self._estadisticas['hits'],
                'misses': self._estadisticas['misses'],
                'escrituras': self._estadisticas['escrituras'],
                'tasa_acierto': round(tasa_acierto, 2),
                'items_en_cache': len(self._datos)
            }
    
    def __repr__(self) -> str:
        """Representación en string del caché"""
        stats = self.obtener_estadisticas()
        return (
            f"Cache(items={stats['items_en_cache']}, "
            f"hits={stats['hits']}, "
            f"misses={stats['misses']}, "
            f"acierto={stats['tasa_acierto']})"
        )


class cache_funciones:
    """
    Decorador para cachear resultados de funciones.
    Útil para operaciones costosas que se llaman frecuentemente.
    """
    
    # Caché global compartida
    _cache_global = Cache()
    
    def __init__(self, ttl: Optional[int] = None):
        """
        Inicializa el decorador.
        
        Args:
            ttl: Tiempo de vida del caché en segundos
            
        Ejemplo:
            @cache_funciones(ttl=600)
            def obtener_productos_populares():
                # Operación costosa
                return productos
        """
        self.ttl = ttl
    
    def __call__(self, func: Callable) -> Callable:
        """Aplica el decorador a una función"""
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generar clave única basada en función y argumentos
            cache_key = f"{func.__name__}_{args}_{kwargs}"
            
            # Intentar obtener del caché
            resultado = self._cache_global.get(cache_key)
            
            if resultado is not None:
                return resultado
            
            # Si no está en caché, ejecutar función
            resultado = func(*args, **kwargs)
            
            # Almacenar en caché
            self._cache_global.set(cache_key, resultado, self.ttl)
            
            return resultado
        
        # Agregar método para limpiar caché como atributo dinámico
        setattr(wrapper, 'limpiar_cache', lambda: self._cache_global.limpiar())
        setattr(wrapper, 'estadisticas', lambda: self._cache_global.obtener_estadisticas())
        
        return wrapper


# Instancia global de caché para usar en la aplicación
cache_global = Cache(ttl_default=300)
