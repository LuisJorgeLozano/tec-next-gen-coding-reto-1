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
contadorVentas = 0
ultimo_error = ""
MODO_DEBUG = False

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


def reiniciar_sistema():
    """Borra todo el estado del sistema (inventario, ventas y folios)."""
    global contadorVentas, ultimo_error
    INVENTARIO.clear()
    VENTAS.clear()
    contadorVentas = 0
    ultimo_error = ""


def agregarProducto(codigo, nombre, precio, stock):
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
    x = {}
    x["codigo"] = codigo
    x["nombre"] = nombre
    x["precio"] = precio
    x["stock"] = stock
    INVENTARIO[codigo] = x
    return True


def eliminar_producto(codigo):
    """Quita un producto del inventario. Regresa False si no existe."""
    global ultimo_error
    if codigo in INVENTARIO:
        del INVENTARIO[codigo]
        return True
    ultimo_error = "producto no existe"
    return False


def actualizar_stock(codigo, cantidad):
    """Suma unidades al stock (o resta si la cantidad es negativa)."""
    global ultimo_error
    if codigo not in INVENTARIO:
        ultimo_error = "producto no existe"
        return False
    aux = INVENTARIO[codigo]["stock"] + cantidad
    if aux < 0:
        ultimo_error = "el stock no puede quedar negativo"
        return False
    INVENTARIO[codigo]["stock"] = aux
    return True


def buscarProducto(texto):
    # busca productos cuyo nombre contenga el texto (sin importar mayusculas)
    temp2 = []
    for k in INVENTARIO:
        if texto.lower() in INVENTARIO[k]["nombre"].lower():
            temp2.append(INVENTARIO[k])
    return temp2


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


def registrar_venta(codigo, cantidad, cliente=""):
    """Registra una venta: valida, cobra, descuenta stock y genera el ticket.

    Si algo falla regresa None y deja el motivo en ultimo_error.
    """
    global contadorVentas
    if not _validar_venta(codigo, cantidad):
        return None
    producto = INVENTARIO[codigo]
    precios = calcular_precios(producto["precio"], cantidad, cliente)
    producto["stock"] = producto["stock"] - cantidad
    contadorVentas = contadorVentas + 1
    venta = {
        "folio": contadorVentas,
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


def cotizar(codigo, cantidad):
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


def calcular_descuento_viejo(monto):
    # NOTA: esta era la formula de descuentos que se uso hasta 2023,
    # ya nadie la llama pero la dejamos por si acaso
    if monto > 800:
        return monto * 0.08
    return 0


# def exportar_txt(ruta):
#     f = open(ruta, "w")
#     for k in INVENTARIO:
#         f.write(k + " - " + str(INVENTARIO[k]["stock"]) + "\n")
#     f.close()
#     return True
