# Bitácora de Refactorización

**Nombre: Luis Jorge Lozano Domínguez**  
**Matrícula:**  
**Fecha: 08 de octubre de 2026**  

---

# Prompt de Diagnóstico

```markdown
# Rol
Actúa como un Desarrollador Senior de Python especialista en código limpio y refactorización.

# Tarea Principal
Analiza el código del proyecto ubicado en la carpeta `src/` para explicarme su funcionamiento general y proponer las refactorizaciones de mayor impacto.

## Fase 1: Análisis y Explicación del Proyecto
1. **Propósito general:** Explica brevemente qué hace este proyecto.
2. **Relación de módulos:** Explica cómo interactúan los archivos `.py` dentro de la carpeta `src/` (`main.py`, `almacen.py`, `gestor.py`, `reportes.py`).

## Fase 2: Diagnóstico de Mejoras (SIN modificar código aún)
Identifica y reporta las principales oportunidades de mejora evaluando estos 5 rubros sencillos:
1. **Dividir funciones largas:** Separar funciones que hacen demasiadas cosas en partes más pequeñas.
2. **Eliminar código duplicado:** Unificar bloques de código o validaciones que se repiten.
3. **Nombres claros:** Renombrar variables y funciones para que su nombre explique qué hacen (usando `snake_case`).
4. **Simplificar `if` complejos:** Hacer que la lógica con muchas condiciones sea fácil y limpia de leer.
5. **Limpiar código que no se usa:** Eliminar funciones, variables o importaciones innecesarias.

Nota: No apliques ningún cambio al código en este paso, únicamente presenta el listado.

## Fase 3: Las 5 Refactorizaciones de Mayor Valor
De las mejoras encontradas, selecciona las 5 que mayor beneficio le traigan al código.

Para cada una presenta:
1. **Ubicación y Problema:** Archivo, función y por qué se puede mejorar.
2. **Propuesta de solución:** Qué cambios harás y por qué.

Espera mi confirmación para proceder a aplicar la primera refactorización.
```

---

# Bitácora de Prompts

## Prompt 1

```markdown
# Rol
Actúa como Desarrollador Senior de Python especialista en refactorización.

# Tarea
En `src/gestor.py`, `registrar_venta` y `cotizar` repiten el mismo cálculo: subtotal → descuento por volumen → IVA. Unifícalo.

# Cambios
1. Debajo del bloque de estado global, crea constantes en MAYÚSCULAS para los números mágicos: IVA = 0.16, UMBRAL_DESCUENTO_ALTO = 1000, DESCUENTO_ALTO = 0.10, UMBRAL_DESCUENTO_MEDIO = 500, DESCUENTO_MEDIO = 0.05, PREFIJO_VIP = "VIP", DESCUENTO_VIP = 0.02, MINIMO_VIP = 200.
2. Crea `calcular_precios(precio: float, cantidad: int, cliente: str = "") -> dict` que regrese subtotal, descuento, impuesto y total.
   - Descuento por volumen con `if/elif`.
   - Condición VIP en una sola línea: `cliente and cliente.startswith(PREFIJO_VIP) and subtotal - descuento > MINIMO_VIP`.
3. Haz que `registrar_venta` y `cotizar` usen `calcular_precios`. `cotizar` NO aplica el descuento VIP (no recibe cliente).

# Restricciones
- El comportamiento debe quedar idéntico, incluido el redondeo: subtotal, descuento e impuesto se redondean a 2 decimales al guardarse, y total = round(base + impuesto, 2).
- No modifiques los tests ni otras funciones.
- Sigue CLAUDE.md: tipado en firmas, comentarios breves en inglés, sin librerías nuevas.

# Verificación
Ejecuta `python3 -m pytest`; deben pasar los 20 tests (sobre todo `test_venta_cliente_vip_recibe_descuento_extra` y `test_cotizar_coincide_con_el_total_de_la_venta`). Muéstrame el diff y el resultado.
```

* **Cambio Realizado:** Unificación del cálculo de montos (subtotal, descuentos por volumen/VIP e IVA) mediante la función helper calcular_precios y el uso de constantes globales para los valores numéricos.
* **Justificación:** Elimina la duplicación de código entre registrar_venta y cotizar, mejora la mantenibilidad centralizando las reglas de negocio financieras y reduce la presencia de números mágicos.
* **Tests OK:** `============================== 20 passed in 0.04s ==============================`

---

## Prompt 2

```markdown
# Rol
Actúa como Desarrollador Senior de Python especialista en código limpio.

# Tarea
En `src/gestor.py`, `registrar_venta` hace demasiadas cosas (valida, calcula, descuenta stock, genera folio, arma la venta y el ticket) y tiene 4 niveles de `if` anidados. Divídela.

# Cambios
1. Extrae _validar_venta(codigo: str, cantidad: int) -> bool usando validaciones independientes y salidas tempranas (return False en cada error). Mantén el MISMO orden y los MISMOS mensajes en ultimo_error: "codigo vacio", "producto no existe", "cantidad invalida", "stock insuficiente".
2. Extrae `_armar_ticket(venta: dict) -> str` usando f-strings. El texto de salida debe ser idéntico al actual, incluida la línea "Descuento" que solo aparece si el descuento > 0.
3. Deja `registrar_venta` como orquestador corto: validar → calcular_precios → descontar stock → incrementar folio → crear dict de venta → ticket → append a VENTAS → return.
4. Quita la inicialización innecesaria `temp2 = None` y la concatenación `t = ""`.

# Restricciones
- Mantener los mismos parámetros en registrar_venta y mismo valor de retorno (dict o None).
- Si la venta falla, el stock no cambia.
- No modifiques los tests. Sigue CLAUDE.md.

# Verificación
Ejecuta `python3 -m pytest` (deben pasar los 20 tests). Muestra el diff y la nueva `registrar_venta` completa.
```

* **Cambio Realizado:** Reestructuración de la función registrar_venta mediante la extracción de las funciones auxiliares _validar_venta y _armar_ticket, la eliminación de variables temporales innecesarias y el ajuste de la firma de restricciones.
* **Justificación:** Elimina el anidamiento excesivo de condicionales, separa las responsabilidades de validación y formato de texto de la lógica principal, y garantiza la compatibilidad con las pruebas existentes al conservar los parámetros y tipos de retorno originales.
* **Tests OK:** `============================== 20 passed in 0.05s ==============================`

---

## Prompt 3

```markdown
# Rol
Actúa como Desarrollador Senior de Python especialista en limpieza de código.

# Tarea
Elimina el código muerto de `src/`. Antes de borrar cada elemento, confirma con una búsqueda (grep en `src/` y `tests/`) que nadie lo usa.

# Elementos a eliminar
- `src/gestor.py`: la función `calcular_descuento_viejo`, el bloque comentado `exportar_txt` y la constante `MODO_DEBUG`.
- `src/reportes.py`: la función `reporteViejoCSV` y el `import os` que no se usa.

# Simplificar
- `src/almacen.py`: `hayArchivo` debe quedar como `return os.path.exists(ruta)` (sin if/else), con tipado `(ruta: str) -> bool`.

# Restricciones
- No cambies el comportamiento ni los nombres públicos que sí se usan.
- No modifiques los tests.

# Verificación
Ejecuta `python3 -m pytest` (deben pasar los 20 tests) y `python3 -c "import sys; sys.path.insert(0,'src'); import main"` para confirmar que no hay errores de importación. Lista lo eliminado y muestra el diff.
```

* **Cambio Realizado:** Eliminación de funciones, bloques y constantes en desuso en el módulo src/, limpieza de importaciones redundantes y simplificación lógica de la función hayArchivo en src/almacen.py.
* **Justificación:** Reduce la deuda técnica eliminando código muerto verificado, optimiza las importaciones para evitar carga innecesaria de módulos y mejora la legibilidad en la verificación de archivos al prescindir de estructuras condicionales redundantes.
* **Tests OK:** `============================== 20 passed in 0.05s ==============================`

---

## Prompt 4

```markdown
# Rol
Actúa como Desarrollador Senior de Python especialista en refactorización.

# Tarea
Elimina la duplicación y la lógica manual en `src/reportes.py`.

# Cambios
1. Crea la constante `STOCK_MINIMO = 5` y úsala en `productos_stock_bajo` y en `reporte_inventario` (hoy ambas tienen `< 5` escrito a mano).
2. `resumen_ventas`: usa `total_vendido()` en lugar de volver a sumar los totales a mano. El texto final debe quedar igual.
3. `mas_vendidos`: reemplaza el ordenamiento de burbuja por `sorted(..., key=lambda par: par[1], reverse=True)` y acumula con `dict.get(codigo, 0)`. Elimina el TODO. `sorted` es estable, así que se respeta el orden actual en empates.
4. Agrega tipado a las firmas de estas funciones.

# Restricciones
- Las salidas (listas, tuplas y textos impresos y devueltos) deben ser idénticas.
- No modifiques los tests. Sigue CLAUDE.md.

# Verificación
Ejecuta `python3 -m pytest` (deben pasar los 20 tests, sobre todo `test_mas_vendidos_ordena_por_unidades` y `test_reporte_inventario_marca_stock_bajo`). Muestra el diff.
```

* **Cambio Realizado:** Reemplazo de la lógica de ordenamiento por burbuja y acumulación manual en mas_vendidos por sorted() y dict.get(), reutilización de total_vendido() en resumen_ventas, centralización del umbral de inventario en la constante STOCK_MINIMO y adición de anotaciones de tipo en las firmas de las funciones de src/reportes.py.
* **Justificación:** Elimina código duplicado y números mágicos centralizando las reglas de inventario, aprovecha las funciones nativas de Python para mejorar la eficiencia del ordenamiento respetando los empates, y refuerza la claridad del código con tipado explícito sin alterar el comportamiento esperado por las pruebas.
* **Tests OK:** `============================== 20 passed in 0.06s ==============================`

---

## Prompt 5

```markdown
# Rol
Actúa como Desarrollador Senior de Python especialista en código legible.

# Tarea
Renombra funciones y variables de `src/` para que sigan `snake_case` y expliquen lo que hacen.

# Renombres de funciones y estado (actualiza TODAS las referencias en src/ y tests/)
- `gestor.agregarProducto` → `agregar_producto`
- `gestor.buscarProducto` → `buscar_producto`
- `gestor.contadorVentas` → `contador_ventas` (también en `almacen.py`; la clave del JSON sigue siendo "contador")
- `almacen.hayArchivo` → `existe_archivo`
- `reportes.hacer_cosa` → `formatear_dinero`

# Renombres de variables locales
- `temp2`, `temp`, `aux`, `t`, `x`, `d`, `f`, `s`, `p`, `desc`, `linea` ambiguos → nombres descriptivos (`producto`, `resultados`, `subtotal`, `valor_total`, `datos`, `archivo`, `texto`, `descuento`, etc.).
- En `main.py`: `c`, `n`, `p`, `s`, `cant`, `cli`, `v`, `op` → `codigo`, `nombre`, `precio`, `stock`, `cantidad`, `cliente`, `venta`, `opcion`.

# Restricciones
- Cambio puramente de nombres: no alteres la lógica.
- En `tests/` solo cambia los nombres de las funciones llamadas; no toques ninguna aserción.
- Agrega tipado a las firmas que toques. Sigue CLAUDE.md.

# Verificación
1. `grep -rnE "agregarProducto|buscarProducto|contadorVentas|hayArchivo|hacer_cosa" src tests` no debe devolver resultados.
2. `python3 -m pytest` debe pasar los 20 tests.
Muestra el diff.
```

* **Cambio Realizado:** Refactorización de nomenclatura en el módulo src/ y en las pruebas para migrar nombres de funciones y variables al estándar snake_case, sustitución de identificadores ambiguos por nombres descriptivos y adición de anotaciones de tipo en las firmas modificadas.
* **Justificación:** Mejora la legibilidad y mantenibilidad del proyecto alineando el código con la convención PEP 8, elimina nombres de variables no descriptivos para facilitar su comprensión y asegura la consistencia en el proyecto mediante la actualización global de referencias sin alterar la lógica de negocio.
* **Tests OK:** `============================== 20 passed in 0.05s ==============================`