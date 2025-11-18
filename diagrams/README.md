# Diagramas PlantUML del Sistema de Gestión de Restaurante

Este directorio contiene los diagramas arquitectónicos del sistema en formato PlantUML. Puedes usar estos diagramas directamente en herramientas como:
- PlantUML online: https://www.plantuml.com/plantuml/uml/
- VS Code con extensión PlantUML
- Editores de diagramas que soportan PlantUML

---

## 📊 Diagramas Disponibles

### 1. **Diagrama de Clases Simple** (`class_diagram.puml`)
Diagrama original con las clases principales del sistema:
- Interfaz IMenu
- Clases de dominio: CrearMenu, Ingrediente, Stock, Pedido
- Patrón Facade: BoletaFacade
- Clase principal: Restaurante

### 2. **Diagrama de Clases Completo** (`class_diagram_complete.puml`)
Versión mejorada con:
- Documentación completa de métodos
- Todas las relaciones
- Notas explicativas
- Colores diferenciados

### 3. **Diagrama de Clases con Mejoras** (`class_diagram_with_improvements.puml`)
Incluye TODOS los módulos del sistema:
- **Dominio**: Clases de negocio
- **Patrones**: Facade, Factory, etc.
- **GUI**: Interfaz gráfica
- **Manejo de Errores**: LoggerConfig, Validador
- **Optimización**: Cache con TTL
- **Utilidades**: Formateo, Cálculos, Archivos
- **Estadísticas**: Módulo de análisis
- **Base de Datos**: Modelos SQLAlchemy

### 4. **Diagrama Entidad-Relación (MER)** (`mer_diagram.puml`)
Modelo de datos relacional con:
- Tabla: Clientes
- Tabla: Pedidos
- Tabla: PedidoItems
- Tabla: Menus
- Tabla: Ingredientes
- Tabla: MenuIngredientes (relación N:M)
- Todas las relaciones y tipos de datos

---

## 🚀 Cómo Usar

### Opción 1: PlantUML Online
1. Abre https://www.plantuml.com/plantuml/uml/
2. Copia el contenido de cualquier archivo .puml
3. Pégalo en el editor
4. Presiona "Render" o espera a que se actualice automáticamente

### Opción 2: VS Code
1. Instala la extensión "PlantUML" (jebbs.plantuml)
2. Abre uno de los archivos .puml
3. Presiona Alt + D para ver la vista previa

### Opción 3: Comando CLI
```bash
# Instala PlantUML si no lo tienes
pip install plantuml

# Genera PNG desde archivo
plantuml -Tpng class_diagram_complete.puml

# Genera SVG (recomendado para web)
plantuml -Tsvg class_diagram_with_improvements.puml
```

---

## 📐 Estructura del MER

```
Clientes (1) ──── (N) Pedidos
  │                      │
  │                      └──── (N) PedidoItems ──── (1) Menus
  │                                                    │
  └────────────────────────────────────────────────── │
                                                       │
                                         (N) MenuIngredientes (N)
                                              │
                                              └──── (1) Ingredientes
```

---

## 🎨 Colores por Package

En el diagrama detallado (`class_diagram_with_improvements.puml`):

| Color | Package | Descripción |
|-------|---------|-------------|
| 🔵 Azul claro | Dominio | Clases de negocio |
| 🌸 Rosa | Patrones | Implementación de patrones de diseño |
| 🟢 Verde | GUI | Interfaz gráfica |
| 🟡 Amarillo | Errores | Manejo y validación |
| 🔷 Azul | Caché | Optimización |
| 💜 Púrpura | Utilidades | Funciones auxiliares |
| 🟠 Naranja | Estadísticas | Análisis de datos |
| 🌹 Rosa fuerte | Base de Datos | Modelos SQLAlchemy |

---

## 📝 Elementos de la Notación

### Relaciones
- `*--` : Composición (relación fuerte)
- `o--` : Agregación (relación débil)  
- `-->` : Asociación
- `..>` : Dependencia

### Cardinalidad
- `1` : Exactamente uno
- `*` : Cero o muchos
- `o{` : Cero o muchos
- `||` : Exactamente uno

### Símbolos
- `interface` : Interfaz/Protocol
- `class` : Clase
- `entity` : Entidad de base de datos
- `package` : Agrupación lógica
- `{static}` : Métodos/atributos estáticos
- `PK` : Primary Key (Clave primaria)
- `FK` : Foreign Key (Clave foránea)
- `UNIQUE` : Restricción de unicidad

---

## 🔄 Relaciones Principales

### Composición de Menú
```
CrearMenu (1) --*-- (*) Ingrediente
  └─ contiene ingredientes con cantidades específicas
```

### Gestión de Pedidos
```
Pedido (1) --*-- (*) CrearMenu
  └─ contiene múltiples menús
  └─ calcula totales e IVA
```

### Stock
```
Stock (1) --*-- (*) Ingrediente
  └─ gestiona inventario centralizado
  └─ verifica disponibilidad
  └─ reserva y libera ingredientes
```

### Base de Datos
```
Cliente (1) ──── (N) Pedido ──── (N) PedidoItem ──── (1) Menu
Menu (N) ──── (N) Ingrediente (a través de MenuIngrediente)
```

---

## 💡 Patrones de Diseño Representados

### Patrones Implementados:

1. **Singleton**: Stock (gestión centralizada)
   - Control centralizado del inventario
   - Única instancia garantizada

2. **Factory**: MenuCatalog (creación de menús)
   - Creación flexible de menús
   - Estandarización de construcción

3. **Facade**: BoletaFacade (simplificación)
   - Interfaz simplificada
   - Oculta complejidad

4. **Protocol/Interface**: IMenu (tipado estructural)
   - Interfaz moderna de Python
   - Tipado estructural flexible

5. **Observer (implícito)**: Actualización automática de GUI
   - Sincronización automática
   - Desacoplamiento de componentes

6. **Decorator**: @cache_funciones, @manejo_errores
   - Funcionalidad transversal
   - Decoradores reutilizables

7. **⭐ NUEVO - Template Method**: `template_method.py` + `error_handler.py`
   - **En error_handler.py** (Integrados):
     - `ValidadorTemplate` - Define flujo de validación
     - 4 validadores específicos (Cantidad, Precio, Nombre, Email)
   - **En template_method.py** (Módulo de referencia completo):
     - `GeneradorReportesTemplate` - Define flujo de generación de reportes
     - 3 generadores de reportes (Pedidos, Productos, Clientes)
   - **Uso**: Los validadores ahora se pueden usar directamente desde error_handler
   - Ver documentación completa en template_method.py y error_handler.py

---

## 📊 Análisis de Complejidad

### Operaciones del Stock
- Agregar ingrediente: **O(1)** (diccionario)
- Verificar disponibilidad: **O(n)** (n = cantidad de ingredientes)
- Reservar ingredientes: **O(n)**

### Operaciones del Pedido
- Agregar menú: **O(1)** (diccionario)
- Calcular total: **O(m)** (m = cantidad de menús)
- Limpiar: **O(1)** (reinicia referencia)

### Caché
- Set/Get: **O(1)** (diccionario)
- Limpieza de expirados: **O(n)** (n = items en caché)

---

## 🔗 Referencias

- **PlantUML**: https://plantuml.com/
- **Documentación**: https://plantuml.com/class-diagram
- **Guía de MER**: https://plantuml.com/er-diagram
- **Sintaxis**: https://plantuml.com/syntax-and-features

---

## 📌 Notas

- Los diagramas se pueden exportar como PNG, SVG, PDF
- SVG es recomendado para incluir en documentación web
- Todos los diagramas están actualizados con las mejoras de la rama `feature/mejoras_codigo`
- Los colores y estilos son configurables en la sección `skinparam`

---

**Última actualización**: Noviembre 2025
**Versión**: 2.0 (con módulos de mejoras)
