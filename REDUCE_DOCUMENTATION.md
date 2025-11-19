#  Documentación: Programación Funcional con `reduce()`

##  ¿Qué es `reduce()`?

`reduce()` es una función de programación funcional que **acumula valores** de un iterable aplicando una función de forma repetida.

```python
from functools import reduce

resultado = reduce(función_acumulativa, iterable, valor_inicial)
```

### Componentes:
- **función_acumulativa**: Toma 2 argumentos (acumulador, elemento actual)
- **iterable**: Secuencia de valores a procesar
- **valor_inicial**: Valor con el que comienza el acumulador

---

##  Ejemplo Visual

```
Secuencia: [1, 2, 3, 4, 5]
Función: suma (lambda acc, x: acc + x)
Inicial: 0

Iteración 1: f(0, 1) = 1
Iteración 2: f(1, 2) = 3
Iteración 3: f(3, 3) = 6
Iteración 4: f(6, 4) = 10
Iteración 5: f(10, 5) = 15
Resultado: 15
```

---

##  Implementaciones en el Proyecto

### 1️ `utilities.py` - `calcular_total_pedido_reduce()`

**Ubicación:** `utilities.py`, línea ~135

**Propósito:** Calcula el total de un pedido usando `reduce()` (versión funcional)

**Código:**

```python
@staticmethod
def calcular_total_pedido_reduce(items: List[Dict]) -> Decimal:
    """Calcula el total de un pedido usando reduce (programación funcional)"""
    
    def acumular_item(total_acum: Decimal, item: Dict) -> Decimal:
        """Función acumulativa: suma el item al total"""
        precio = Decimal(str(item.get('precio', 0)))
        cantidad = Decimal(str(item.get('cantidad', 1)))
        descuento = Decimal(str(item.get('descuento', 0)))
        
        subtotal = precio * cantidad
        descuento_monto = (subtotal * descuento) / Decimal('100')
        
        return total_acum + (subtotal - descuento_monto)
    
    # Usar reduce() para acumular todos los items
    if not items:
        return Decimal('0.00')
    
    total = reduce(acumular_item, items, Decimal('0'))
    return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
```

**Uso:**

```python
from utilities import UtilCalculos

items = [
    {'precio': 100, 'cantidad': 2},
    {'precio': 50, 'cantidad': 1, 'descuento': 10}
]

# Versión con reduce
total_funcional = UtilCalculos.calcular_total_pedido_reduce(items)
print(f"Total: ${total_funcional}")  # Total: $240.00

# Versión tradicional (también disponible)
total_tradicional = UtilCalculos.calcular_total_pedido(items)
print(f"Total: ${total_tradicional}")  # Total: $240.00 (igual resultado)
```

---

### 2️ `template_method.py` - `GeneradorReportesTemplate._formatear_reporte()`

**Ubicación:** `template_method.py`, línea ~275

**Propósito:** Acumular totales de múltiples pedidos usando `reduce()`

**Código:**

```python
def _formatear_reporte(self, datos: List[Any], parametros: Dict) -> Dict[str, Any]:
    """Formatea los datos en estructura de reporte usando reduce para cálculos"""
    
    # Función acumulativa que suma montos e IVAs
    def acumular_totales(acc, pedido):
        return {
            'monto_total': acc['monto_total'] + pedido['monto'],
            'iva_total': acc['iva_total'] + pedido['iva']
        }
    
    # Si hay datos, calcular totales con reduce
    if datos:
        totales = reduce(
            acumular_totales,
            datos,
            {'monto_total': 0, 'iva_total': 0}
        )
        total_monto = totales['monto_total']
        total_iva = totales['iva_total']
    else:
        total_monto = 0
        total_iva = 0
    
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
```

**Uso:**

```python
from template_method import GeneradorReportesTemplate

# Crear instancia
generador = GeneradorReportesTemplate()

# Datos de ejemplo
pedidos = [
    {'id': 1, 'cliente': 'Juan', 'monto': 50000, 'fecha': datetime.now(), 'monto_con_iva': 59500, 'iva': 9500},
    {'id': 2, 'cliente': 'María', 'monto': 75000, 'fecha': datetime.now(), 'monto_con_iva': 89250, 'iva': 14250},
    {'id': 3, 'cliente': 'Pedro', 'monto': 60000, 'fecha': datetime.now(), 'monto_con_iva': 71400, 'iva': 11400},
]

# Generar reporte (internamente usa reduce para acumular)
reporte = generador.generar_reporte(pedidos)

# Ver resumen
print(f"Total: ${reporte['resumen']['monto_total']}")  # Total: $185000
print(f"IVA: ${reporte['resumen']['iva_total']}")      # IVA: $35150
```

---

##  Comparación: Loop vs sum() vs reduce()

### Caso: Calcular total de pedido

**1️ CON LOOP TRADICIONAL** (Imperativo)
```python
total = 0
for item in items:
    total += item['precio'] * item['cantidad']
# total = 250
```
Legible para principiantes
Fácil de debuggear
Más verboso

---

**2️ CON sum()** (Pythonic, RECOMENDADO)
```python
total = sum(item['precio'] * item['cantidad'] for item in items)
# total = 250
```
 Conciso y legible
 Idiomatic Python
 Buena performance
 Limitado a casos simples

---

**3️ CON reduce()** (Funcional)
```python
from functools import reduce

total = reduce(
    lambda acc, item: acc + (item['precio'] * item['cantidad']),
    items,
    0
)
# total = 250
```
 Programación funcional pura
 Muy flexible
 Menos legible
 Curva de aprendizaje más alta

---

##  Recomendaciones

| Caso | Usar |
|------|------|
| **Suma simple** |  `sum()` |
| **Promedio, máximo, mínimo** |  `sum()`, `max()`, `min()` |
| **Operación iterativa compleja** |  `loop for` |
| **Acumular diccionarios** |  `reduce()` |
| **Pipeline funcional** | `reduce()` |
| **Cálculos financieros con precisión** |  `reduce()` (con Decimal) |

---

##  Casos de Uso Prácticos

### Caso 1: Acumular Moneda Decimal (Precisión Financiera)
```python
from functools import reduce
from decimal import Decimal

pedidos = [
    {'monto': Decimal('99.99')},
    {'monto': Decimal('49.99')},
    {'monto': Decimal('29.99')},
]

total = reduce(
    lambda acc, p: acc + p['monto'],
    pedidos,
    Decimal('0')
)
# total = Decimal('179.97')
```

### Caso 2: Agrupar y Contar
```python
datos = [
    {'categoria': 'A', 'valor': 10},
    {'categoria': 'B', 'valor': 20},
    {'categoria': 'A', 'valor': 15},
    {'categoria': 'B', 'valor': 25},
]

por_categoria = reduce(
    lambda acc, item: {
        **acc,
        item['categoria']: acc.get(item['categoria'], 0) + item['valor']
    },
    datos,
    {}
)
# {'A': 25, 'B': 45}
```

### Caso 3: Aplicar Descuentos Secuenciales
```python
precio_inicial = 1000

# Aplicar descuentos: 10%, 5%, 2%
descuentos = [0.10, 0.05, 0.02]

precio_final = reduce(
    lambda precio, descuento: precio * (1 - descuento),
    descuentos,
    precio_inicial
)
# precio_final ≈ 833.88
```

---

##  Errores Comunes

### Error 1: No manejar lista vacía
```python
# INCORRECTO
total = reduce(lambda a, b: a + b, [])  # ValueError!

# CORRECTO
total = reduce(lambda a, b: a + b, [], 0)  # Retorna 0
```

###  Error 2: Olvidar valor inicial
```python
# INCORRECTO - Asume primer elemento como inicial
resultado = reduce(lambda a, b: a + b, numeros)

# CORRECTO - Especificar inicial
resultado = reduce(lambda a, b: a + b, numeros, 0)
```

###  Error 3: Función acumulativa con tipo incorrecto
```python
# INCORRECTO - Acumulador y elemento tienen tipos diferentes
reduce(lambda acc, item: acc + item['precio'], items, 0)  # Error!

# CORRECTO - Especificar tipo correcto del inicial
reduce(lambda acc, item: acc + item['precio'], items, Decimal('0'))
```

---

##  Performance

Para la mayoría de operaciones, la diferencia es mínima:

```
Operación: Sumar 1,000,000 números

Loop for:      ~50ms
sum():         ~45ms  ← MEJOR
reduce():      ~52ms
```

**Conclusión:** Usar lo que sea más legible. Performance es similar.

---

##  Referencias

- [Python docs: functools.reduce()](https://docs.python.org/3/library/functools.html#functools.reduce)
- [Functional Programming in Python](https://realpython.com/python-functional-programming/)
- [Reduce en Python - Real Python](https://realpython.com/map-filter-reduce/)

---

##  Resumen

**`reduce()` es útil para:**
- Acumular valores de forma funcional
- Operaciones iterativas complejas
- Cálculos con precisión decimal
- Código que sigue paradigma funcional

 **Usar en el proyecto cuando:**
- Necesites acumular diccionarios complejos
- Trabajes con Decimal para precisión monetaria
- El código sea más legible que alternativas

 **Evitar cuando:**
- Basta con `sum()`, `max()`, `min()`
- El código sea menos legible que un loop

