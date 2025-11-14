# Sistema de Gestión de Restaurante 🍽️

Sistema completo de gestión para restaurantes implementado en Python, con interfaz gráfica moderna (CustomTkinter) y patrones de diseño profesionales.

## 📋 Características

- ✅ Gestión centralizada de inventario (Patrón Singleton)
- ✅ Creación dinámica de menú (Patrón Factory)
- ✅ Generación de boletas en PDF (Patrón Facade)
- ✅ Sincronización automática de UI (Patrón Observer)
- ✅ Carga de inventario desde CSV
- ✅ Visor PDF integrado
- ✅ Manejo robusto de errores
- ✅ Sistema de caché para optimizar performance
- ✅ Base de datos SQLAlchemy
- ✅ Estadísticas y reportes

## 🏗️ Arquitectura

### Patrones de Diseño

1. **Singleton (Stock)**
   - Control centralizado del inventario
   - Garantiza una única instancia de gestión de stock
   - Thread-safe para operaciones concurrentes

2. **Factory (Menu_catalog)**
   - Creación flexible de elementos de menú
   - Fácil extensión de nuevos productos
   - Estandarización de construcción

3. **Facade (BoletaFacade)**
   - Interfaz simplificada para generación de boletas
   - Oculta complejidad de múltiples operaciones
   - Coordina creación de PDF y actualización de stock

4. **Observer (Restaurante.py)**
   - Sincronización automática de UI
   - Notificación de cambios en tiempo real
   - Desacoplamiento de componentes

## 📁 Estructura de Archivos

```
ev2_progra2/
├── Restaurante.py           # Aplicación principal y GUI
├── Stock.py                 # Gestión de inventario (Singleton)
├── Menu_catalog.py          # Catálogo de menú (Factory)
├── BoletaFacade.py          # Generación de boletas (Facade)
├── Pedido.py                # Gestión de órdenes
├── ElementoMenu.py          # Elemento de menú
├── Ingrediente.py           # Componentes base
├── error_handler.py         # Manejo centralizado de errores ⭐ NUEVO
├── utilities.py             # Funciones de utilidad reutilizables ⭐ NUEVO
├── cache_manager.py         # Sistema de caché con TTL ⭐ NUEVO
├── database.py              # Configuración de base de datos
├── models.py                # Modelos SQLAlchemy
├── crud.py                  # Operaciones CRUD
├── statistics_tab.py        # Módulo de estadísticas
├── ctk_pdf_viewer.py        # Visor PDF personalizado
├── menu_pdf.py              # Generación de menú en PDF
├── ingredientes_menu.csv    # Datos de ingredientes
├── IMG/                     # Iconos y imágenes
└── informe_latex/           # Presentación y documentación
```

## 🚀 Instalación

### Requisitos
- Python 3.8+
- pip

### Dependencias

```bash
pip install customtkinter
pip install pandas
pip install pillow
pip install sqlalchemy
pip install reportlab
pip install pymupdf
```

### Instalación rápida

```bash
# Clonar repositorio
git clone https://github.com/Zywite/evaluacion_2.git
cd ev2_progra2

# Crear entorno virtual
python -m venv .venv

# Activar entorno
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## 📖 Uso

### Iniciar aplicación

```bash
python Restaurante.py
```

### Cargar inventario desde CSV

1. Haz clic en "Cargar CSV"
2. Selecciona archivo con formato:
   ```
   nombre,cantidad,precio
   Hamburguesa,10,5000
   Pizza,15,8000
   ```

### Crear pedido

1. Selecciona productos del menú
2. Haz clic en "Agregar al Pedido"
3. El sistema verifica stock automáticamente
4. Visualiza total en tiempo real

### Generar boleta

1. Revisa items del pedido
2. Haz clic en "Generar Boleta"
3. Se crea PDF automáticamente
4. Vista previa integrada

## 🛠️ Nuevos Módulos (Mejoras)

### 1️⃣ error_handler.py - Manejo de Errores
Centraliza toda la validación y manejo de excepciones

```python
from error_handler import Validador, logger, manejo_errores, MensajesError

# Validar entrada
try:
    cantidad = Validador.validar_cantidad(input_user)
    precio = Validador.validar_precio(input_price)
except ValueError as e:
    titulo, msg = MensajesError.CANTIDAD_INVALIDA
    mostrar_error(titulo, msg)

# Usar decorador para auto-captura de errores
@manejo_errores
def procesar_pedido():
    pass

# Logging automático
logger.info("Operación completada exitosamente")
logger.error("Error procesando pedido", exc_info=True)
```

**Características:**
- Excepciones personalizadas (StockException, PedidoException, etc.)
- Mensajes de error consistentes
- Validadores reutilizables
- Logging automático a archivo y consola
- Decorador para manejo transparente de errores

### 2️⃣ utilities.py - Documentación y Utilidades
Módulo completamente documentado con funciones reutilizables

```python
from utilities import (
    UtilFormatter, UtilCalculos, UtilArchivos, UtilValidacion
)

# Formateo de datos
UtilFormatter.formatear_precio(1500.50)  # "$1.500,50"
UtilFormatter.formatear_cantidad(10.5)   # "10.50"

# Cálculos monetarios con precisión
items = [
    {'precio': 100, 'cantidad': 2},
    {'precio': 50, 'cantidad': 1, 'descuento': 10}
]
total = UtilCalculos.calcular_total_pedido(items)

# Validación de entrada
if UtilValidacion.es_positivo(monto):
    precio = UtilCalculos.aplicar_descuento(monto, 10)

# Operaciones con archivos
UtilArchivos.crear_directorio_si_no_existe("./reportes")
nombre = UtilArchivos.obtener_nombre_archivo(ruta)
```

**Funciones documentadas:**
- UtilFormatter: Formateo de precios, cantidades, extensiones
- UtilCalculos: Totales, descuentos, cálculos monetarios
- UtilArchivos: Operaciones con archivos
- UtilValidacion: Validación de entrada

### 5️⃣ cache_manager.py - Optimización de Performance
Sistema de caché thread-safe con TTL

```python
from cache_manager import cache_funciones, cache_global

# Decorador para cachear resultados de función
@cache_funciones(ttl=600)  # 10 minutos
def obtener_productos_populares():
    # Operación costosa (query BD)
    return db.query(Producto).filter(...).all()

# Caché manual
cache_global.set('usuario_1', {'nombre': 'Juan'}, ttl=300)
usuario = cache_global.get('usuario_1')

# Limpiar items expirados
items_limpios = cache_global.limpiar_expirados()

# Ver estadísticas
stats = cache_global.obtener_estadisticas()
print(f"Tasa de acierto: {stats['tasa_acierto']}")  # 0.86 (86%)
```

**Características:**
- TTL (Time To Live) configurable
- Thread-safe para operaciones concurrentes
- Decorador para cachear funciones automáticamente
- Estadísticas de uso (hits, misses, tasa de acierto)
- Limpieza automática de items expirados

## 📊 Estadísticas

El módulo `statistics_tab.py` proporciona:
- Análisis de ventas
- Productos más vendidos
- Ingresos por período
- Tendencias de consumo

## 🧪 Testing

### Ejecutar tests

```bash
python -m pytest tests/ -v
```

### Coverage

```bash
python -m pytest tests/ --cov=. --cov-report=html
```

## 🔒 Seguridad

- Validación de entrada en todos los campos
- Manejo thread-safe de operaciones críticas
- Logging de operaciones importantes
- Excepciones personalizadas y detalladas

## 📈 Performance

- Sistema de caché con TTL (Time To Live)
- Queries optimizadas en base de datos
- Lazy loading de datos
- Actualización selectiva de UI

Ejemplo de impacto:
```python
# Sin caché: ~500ms por query
# Con caché: ~1ms para cache hit
# Tasa de acierto típica: 85-90%
```

## 🐛 Debugging

### Habilitar logs detallados

Los logs se guardan automáticamente en `restaurante.log`:

```python
from error_handler import logger

logger.debug("Información de debug")
logger.info("Información general")
logger.warning("Advertencia")
logger.error("Error crítico")
```

## 📝 Git Workflow

```bash
# Crear rama para mejoras
git checkout -b feature/mejoras-codigo

# Cambios y commits
git add .
git commit -m "Agrego validación, documentación y caché"

# Push y Pull Request
git push origin feature/mejoras-codigo
```

## 🤝 Contribuciones

1. Fork del proyecto
2. Crear rama: `git checkout -b feature/AmazingFeature`
3. Commit: `git commit -m 'Add AmazingFeature'`
4. Push: `git push origin feature/AmazingFeature`
5. Pull Request

## 📄 Licencia

Este proyecto es parte de la evaluación de Programación II en la Universidad Católica de Temuco.

## ✍️ Autores

- **Joaquín Burgos**
- **Benjamín Cabrera**
- **Leonardo Chávez**

**Profesor:** Guido Mellado  
**Asignatura:** Programación II  
**Institución:** Universidad Católica de Temuco

## 📞 Soporte

Para reportar bugs o sugerencias, abre un issue en GitHub.

---

**Última actualización:** Noviembre 2025  
**Versión:** 2.0  
**Estado:** En desarrollo - Mejoras implementadas ⭐Para ejecutar el programa:
```bash
python Restaurante.py
```

## Estructura del Proyecto

- `Restaurante.py`: Aplicación principal y GUI
- `BoletaFacade.py`: Generación de boletas
- `ElementoMenu.py`: Definición de elementos del menú
- `Ingrediente.py`: Clase para ingredientes
- `Menu_catalog.py`: Catálogo de menús
- `Pedido.py`: Gestión de pedidos
- `Stock.py`: Control de inventario
- `menu_pdf.py`: Generación de PDFs

## Autores

- Joaquin Carrasco Duran
- Benjamin Cabrera
- Leonardo Chavez

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
