# Guía del Proyecto & Instrucciones para Claude

## Comandos Principales
- **Instalar dependencias:** `pip3 install -r requirements.txt`
- **Ejecutar aplicación:** `python3 src/main.py`
- **Ejecutar pruebas:** `python3 -m pytest`
- **Ejecutar prueba específica:** `python3 -m pytest tests/test_almacen.py`

## Estructura del Proyecto
- `src/`: Contiene la lógica interna de la aplicación.
  - `main.py`: Menú interactivo en terminal para la navegación del usuario.
  - `almacen.py`: Módulo encargado del almacenamiento y carga de información en formato JSON.
  - `gestor.py`: Núcleo de la lógica para el control de inventario y registro de ventas.
  - `reportes.py`: Módulo para la elaboración de reportes de desempeño e indicadores.
- `tests/`: Suite de pruebas automatizadas mediante `pytest`.
- `datos_ejemplo.json`: Conjunto de datos base para realizar pruebas en el menú interactivo.
- `requirements.txt`: Especificación de paquetes y librerías necesarias.
- `BITACORA_TEMPLATE.md`: Formato estructurado para documentar la bitácora de prompts utilizada.

## Reglas de Código
- **Estilo y Nombres:** Usa minúsculas con guiones bajos para variables y funciones (`user_name`), y MAYÚSCULAS para constantes (`MAX_LIMIT`).
- **Simplicidad:** Prioriza un código limpio, legible y fácil de entender, agregando comentarios breves en inglés donde ayude a explicar la lógica.
- **Tipado básico:** Indica el tipo de datos que reciben y devuelven las funciones principales (ej. `def calculate_total(price: float, quantity: int) -> float:`).
- **Manejo de errores:** Captura errores específicos con bloques `try/except` y muestra mensajes claros en consola.

## Restricciones
- **Librerías:** NO instales ni importes librerías externas que no estén listadas en `requirements.txt`.
- **Seguridad:** NO agregues credenciales ni claves de API directamente en el código; utiliza variables de entorno o un archivo `.env`.