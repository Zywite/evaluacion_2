# 📊 Guía Rápida - Diagramas PlantUML

## Archivos Creados

```
diagrams/
├── class_diagram.puml                    # Diagrama simple original
├── class_diagram_complete.puml           # Versión mejorada ⭐ NUEVO
├── class_diagram_with_improvements.puml  # Con todos los módulos ⭐ NUEVO
├── mer_diagram.puml                      # Entidad-Relación ⭐ NUEVO
├── system_explanation.puml               # Explicación del sistema
├── README.md                             # Documentación completa ⭐ NUEVO
└── PLANTUML_CODES.txt                    # Códigos listos para copiar ⭐ NUEVO
```

---

## 🚀 Uso Rápido

### Opción 1: PlantUML Online (Más Fácil)
```bash
1. Abre https://www.plantuml.com/plantuml/uml/
2. Abre diagrams/PLANTUML_CODES.txt
3. Copia el código de un diagrama (entre @startuml y @enduml)
4. Pégalo en el editor online
5. ¡Listo! Se genera automáticamente
```

### Opción 2: VS Code (Recomendado)
```bash
# Instala la extensión
1. Abre VS Code
2. Extensions → Busca "PlantUML"
3. Instala "PlantUML" (jebbs.plantuml)
4. Abre cualquier archivo .puml en diagrams/
5. Alt + D para ver vista previa
```

### Opción 3: Comando CLI
```bash
# Instala PlantUML
pip install plantuml

# Genera PNG
cd diagrams
plantuml -Tpng class_diagram_complete.puml

# Genera SVG (mejor para web)
plantuml -Tsvg mer_diagram.puml

# Genera todos
plantuml -Tsvg *.puml
```

---

## 📋 Diagramas Disponibles

### 1️⃣ **Diagrama de Clases Simple**
- **Archivo**: `class_diagram.puml`
- **Contenido**: Clases principales básicas
- **Uso**: Entender la estructura simple
- **Relaciones**: Stock, Pedido, CrearMenu, Ingrediente

### 2️⃣ **Diagrama de Clases Completo**
- **Archivo**: `class_diagram_complete.puml`
- **Contenido**: Todas las clases del sistema
- **Uso**: Referencia detallada
- **Notas**: Explicaciones en cada clase
- **Mejor que**: class_diagram.puml

### 3️⃣ **Diagrama con Mejoras** ⭐ NUEVO
- **Archivo**: `class_diagram_with_improvements.puml`
- **Contenido**: TODO el sistema dividido en packages:
  - 🔵 Dominio (lógica de negocio)
  - 🌸 Patrones (Facade, Factory)
  - 🟢 GUI (interfaz gráfica)
  - 🟡 Errores (error_handler)
  - 🔷 Caché (cache_manager)
  - 💜 Utilidades (utilities)
  - 🟠 Estadísticas (statistics_tab)
  - 🌹 Base de Datos (SQLAlchemy)
- **Uso**: Visión completa con todas las mejoras
- **Mejor visualización**: VS Code o PlantUML online

### 4️⃣ **Diagrama Entidad-Relación** ⭐ NUEVO
- **Archivo**: `mer_diagram.puml`
- **Contenido**: Modelo de base de datos
- **Tablas**:
  - Clientes
  - Pedidos
  - PedidoItems
  - Menus
  - Ingredientes
  - MenuIngredientes
- **Relaciones**: 1:N, N:M entre tablas
- **Uso**: Entender estructura de BD

---

## 🎯 Qué Diagrama Usar

| Necesidad | Diagrama |
|-----------|----------|
| Entender clases simples | `class_diagram.puml` |
| Referencia detallada de clases | `class_diagram_complete.puml` |
| Ver TODO el sistema | `class_diagram_with_improvements.puml` |
| Estructura de base de datos | `mer_diagram.puml` |
| Copiar código rápido | `PLANTUML_CODES.txt` |

---

## 📊 Estructura del MER Visual

```
┌─────────────┐
│  Clientes   │
│ PK: id      │
├─────────────┤
│ nombre      │
│ apellido    │
│ email (UQ)  │
└──────┬──────┘
       │ 1:N
       │
┌──────┴──────────┐
│    Pedidos      │
│  PK: id         │
├─────────────────┤
│  FK: cliente_id │
│  fecha          │
│  estado         │
│  total          │
└──────┬──────────┘
       │ 1:N
       │
┌──────┴──────────────┐
│  PedidoItems        │
│  PK: id             │
├─────────────────────┤
│  FK: pedido_id      │
│  FK: menu_id        │
│  cantidad           │
│  precio_unitario    │
└──────┬──────────────┘
       │
       │ 1:N
       │
┌──────┴──────┐
│   Menus     │
│ PK: id      │
├─────────────┤
│ nombre (UQ) │
│ precio      │
│ icono_path  │
└──────┬──────┘
       │ N:M (mediante MenuIngredientes)
       │
┌──────┴────────────────┐
│ MenuIngredientes      │
│ PK: menu_id, ing_id   │
├───────────────────────┤
│ FK: menu_id           │
│ FK: ingrediente_id    │
│ cantidad_necesaria    │
└───────────┬───────────┘
            │
            │ N:1
            │
      ┌─────┴────────┐
      │ Ingredientes │
      │  PK: id      │
      ├──────────────┤
      │  nombre (UQ) │
      │  unidad      │
      │  cantidad    │
      └──────────────┘
```

---

## 💡 Colores en class_diagram_with_improvements.puml

```
🔵 #ECEFF1 = Dominio (Clases de negocio)
🌸 #FCE4EC = Patrones de Diseño (Facade, Factory)
🟢 #C8E6C9 = GUI (Interfaz Gráfica)
🟡 #FFECB3 = Manejo de Errores (error_handler)
🔷 #B3E5FC = Optimización (cache_manager)
💜 #E1BEE7 = Utilidades (utilities)
🟠 #FFE0B2 = Estadísticas (statistics_tab)
🌹 #F8BBD0 = Base de Datos (SQLAlchemy)
```

---

## 📈 Cardinalidad en MER

```
||--o{  = 1 a N (Uno a muchos)
}o--||  = N a 1 (Muchos a uno)
o--o   = N a N (Muchos a muchos)
--     = Relación
```

---

## 🔍 Elementos Principales

### Diagrama de Clases
- **interface** : Define contrato (IMenu con Protocol)
- **class** : Implementaciones concretas
- **-** : Privado
- **+** : Público
- **{static}** : Estático (método/atributo de clase)

### MER
- **PK** : Primary Key (Clave primaria)
- **FK** : Foreign Key (Clave foránea)
- **UNIQUE** : Restricción de unicidad
- **NULLABLE** : Puede ser NULL

---

## 📝 Ejemplos de Exportación

### Generar PNG desde CLI
```bash
plantuml -Tpng diagrams/class_diagram_complete.puml
# Genera: diagrams/class_diagram_complete.png
```

### Generar SVG (recomendado para web)
```bash
plantuml -Tsvg diagrams/mer_diagram.puml
# Genera: diagrams/mer_diagram.svg
```

### Generar PDF
```bash
plantuml -Tpdf diagrams/class_diagram_with_improvements.puml
# Genera: diagrams/class_diagram_with_improvements.pdf
```

---

## 🎓 Aprendizaje

### Para Principiantes
1. Empieza con `class_diagram.puml` (simple)
2. Luego ve `class_diagram_complete.puml` (detallado)
3. Estudia `mer_diagram.puml` (base de datos)

### Para Entender la Arquitectura
1. Lee `class_diagram_with_improvements.puml` (visión completa)
2. Identifica cada package (color)
3. Sigue las relaciones entre clases

### Para Desarrollo
1. Usa `mer_diagram.puml` para queries SQL
2. Usa `class_diagram_complete.puml` para código
3. Consulta `PLANTUML_CODES.txt` para templates rápidos

---

## 🔗 Recursos Útiles

- **PlantUML Oficial**: https://plantuml.com/
- **Sintaxis de Diagramas**: https://plantuml.com/class-diagram
- **MER en PlantUML**: https://plantuml.com/er-diagram
- **Generador Online**: https://www.plantuml.com/plantuml/uml/
- **Extensión VS Code**: https://marketplace.visualstudio.com/items?itemName=jebbs.plantuml

---

## ✅ Checklist de Uso

- [ ] Instalé PlantUML o accedí a versión online
- [ ] Puedo visualizar `class_diagram_complete.puml`
- [ ] Puedo visualizar `mer_diagram.puml`
- [ ] Entiendo la estructura de clases
- [ ] Entiendo la estructura de base de datos
- [ ] Puedo exportar a PNG/SVG/PDF

---

**Creado**: Noviembre 2025  
**Versión**: 2.0 (con módulos de mejoras)  
**Estado**: ✅ Completo y listo para usar
