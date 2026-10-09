# -*- coding: utf-8 -*-
"""Modulo principal del gestor de inventario y ventas de "La Esquina".

Aqui vive casi toda la logica del negocio. Historicamente este archivo
lo fueron parchando varias personas, asi que hay de todo un poco.
"""

from datetime import datetime

# ---------------------------------------------------------------
# Estado global de la aplicacion (inventario, ventas y contadores)
# ---------------------------------------------------------------
INVENTARIO = {}
VENTAS = []
contador_ventas = 0
ultimo_error = ""

# ---------------------------------------------------------------
# Reglas de precios (impuestos y descuentos)
# ---------------------------------------------------------------
IVA = 0.16
UMBRAL_DESCUENTO_ALTO = 1000
DESCUENTO_ALTO = 0.10
UMBRAL_DESCUENTO_MEDIO = 500
DESCUENTO_MEDIO = 0.05
PREFIJO_VIP = "VIP"
DESCUENTO_VIP = 0.02
MINIMO_VIP = 200


def calcular_precios(precio: float, cantidad: int, cliente: str = "") -> dict:
    """Calcula subtotal, descuento, impuesto y total de una compra."""
    subtotal = precio * cantidad
    # volume discount
    descuento = 0
    if subtotal >= UMBRAL_DESCUENTO_ALTO:
        descuento = subtotal * DESCUENTO_ALTO
    elif subtotal >= UMBRAL_DESCUENTO_MEDIO:
        descuento = subtotal * DESCUENTO_MEDIO
    # VIP extra applies only if the discounted amount exceeds the minimum
    if cliente and cliente.startswith(PREFIJO_VIP) and subtotal - descuento > MINIMO_VIP:
        descuento = descuento + subtotal * DESCUENTO_VIP
    base = subtotal - descuento
    impuesto = base * IVA
    return {
        "subtotal": subtotal,
        "descuento": descuento,
        "impuesto": impuesto,
        "total": round(base + impuesto, 2),
    }


def reiniciar_sistema() -> None:
    """Borra todo el estado del sistema (inventario, ventas y folios)."""
    global contador_ventas, ultimo_error
    INVENTARIO.clear()
    VENTAS.clear()
    contador_ventas = 0
    ultimo_error = ""


def agregar_producto(codigo: str, nombre: str, precio: float, stock: int) -> bool:
    # valida los datos y da de alta un producto en el inventario
    global ultimo_error
    if codigo is None or codigo == "":
        ultimo_error = "codigo vacio"
        return False
    if codigo in INVENTARIO:
        ultimo_error = "el producto ya existe"
        return False
    if precio <= 0:
        ultimo_error = "precio invalido"
        return False
    if stock < 0:
        ultimo_error = "stock invalido"
        return False
    producto = {}
    producto["codigo"] = codigo
    producto["nombre"] = nombre
    producto["precio"] = precio
    producto["stock"] = stock
    INVENTARIO[codigo] = producto
    return True


def eliminar_producto(codigo: str) -> bool:
    """Quita un producto del inventario. Regresa False si no existe."""
    global ultimo_error
    if codigo in INVENTARIO:
        del INVENTARIO[codigo]
        return True
    ultimo_error = "producto no existe"
    return False


def actualizar_stock(codigo: str, cantidad: int) -> bool:
    """Suma unidades al stock (o resta si la cantidad es negativa)."""
    global ultimo_error
    if codigo not in INVENTARIO:
        ultimo_error = "producto no existe"
        return False
    nuevo_stock = INVENTARIO[codigo]["stock"] + cantidad
    if nuevo_stock < 0:
        ultimo_error = "el stock no puede quedar negativo"
        return False
    INVENTARIO[codigo]["stock"] = nuevo_stock
    return True


def buscar_producto(texto: str) -> list:
    # case-insensitive search of products whose name contains the text
    resultados = []
    for codigo in INVENTARIO:
        if texto.lower() in INVENTARIO[codigo]["nombre"].lower():
            resultados.append(INVENTARIO[codigo])
    return resultados


def _validar_venta(codigo: str, cantidad: int) -> bool:
    """Revisa que la venta sea posible. Deja el motivo en ultimo_error si no."""
    global ultimo_error
    if codigo is None or codigo == "":
        ultimo_error = "codigo vacio"
        return False
    if codigo not in INVENTARIO:
        ultimo_error = "producto no existe"
        return False
    if cantidad is None or cantidad <= 0:
        ultimo_error = "cantidad invalida"
        return False
    if INVENTARIO[codigo]["stock"] < cantidad:
        ultimo_error = "stock insuficiente"
        return False
    return True


def _armar_ticket(venta: dict) -> str:
    """Arma el ticket en texto plano a partir de los datos de la venta."""
    ticket = "TIENDA LA ESQUINA\n"
    ticket += "----------------------------\n"
    ticket += f"Folio: {venta['folio']}\n"
    ticket += f"{venta['nombre']} x{venta['cantidad']}\n"
    ticket += f"Subtotal: ${venta['subtotal']}\n"
    # discount line only shows when there is a discount
    if venta["descuento"] > 0:
        ticket += f"Descuento: -${venta['descuento']}\n"
    ticket += f"IVA: ${venta['impuesto']}\n"
    ticket += f"TOTAL: ${venta['total']}\n"
    return ticket


def registrar_venta(codigo: str, cantidad: int, cliente: str = "") -> dict | None:
    """Registra una venta: valida, cobra, descuenta stock y genera el ticket.

    Si algo falla regresa None y deja el motivo en ultimo_error.
    """
    global contador_ventas
    if not _validar_venta(codigo, cantidad):
        return None
    producto = INVENTARIO[codigo]
    precios = calcular_precios(producto["precio"], cantidad, cliente)
    producto["stock"] = producto["stock"] - cantidad
    contador_ventas = contador_ventas + 1
    venta = {
        "folio": contador_ventas,
        "codigo": codigo,
        "nombre": producto["nombre"],
        "cantidad": cantidad,
        "subtotal": round(precios["subtotal"], 2),
        "descuento": round(precios["descuento"], 2),
        "impuesto": round(precios["impuesto"], 2),
        "total": precios["total"],
        "cliente": cliente,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    venta["ticket"] = _armar_ticket(venta)
    VENTAS.append(venta)
    return venta


def cotizar(codigo: str, cantidad: int) -> float | None:
    """Calcula cuanto costaria una compra sin registrar la venta."""
    global ultimo_error
    if codigo not in INVENTARIO:
        ultimo_error = "producto no existe"
        return None
    if cantidad is None or cantidad <= 0:
        ultimo_error = "cantidad invalida"
        return None
    # quotes never apply the VIP discount
    return calcular_precios(INVENTARIO[codigo]["precio"], cantidad)["total"]
