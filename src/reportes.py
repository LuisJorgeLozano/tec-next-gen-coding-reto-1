# -*- coding: utf-8 -*-
"""Reportes de la tienda: inventario, ventas y mas vendidos."""

import gestor

# Products with stock below this value are flagged as low stock
STOCK_MINIMO = 5


def formatear_dinero(monto: float) -> str:
    # formats a number as money, e.g. 12.5 -> "$12.5"
    return "$" + str(round(monto, 2))


def productos_stock_bajo() -> list:
    """Regresa la lista de productos con stock por debajo del minimo."""
    productos_bajos = []
    for codigo in gestor.INVENTARIO:
        if gestor.INVENTARIO[codigo]["stock"] < STOCK_MINIMO:
            productos_bajos.append(gestor.INVENTARIO[codigo])
    return productos_bajos


def reporte_inventario() -> str:
    """Arma el reporte del inventario, lo imprime y lo regresa como texto."""
    texto = "===== INVENTARIO =====\n"
    valor_total = 0
    for codigo in gestor.INVENTARIO:
        producto = gestor.INVENTARIO[codigo]
        linea = producto["codigo"] + " | " + producto["nombre"] + " | "
        linea = linea + formatear_dinero(producto["precio"]) + " | stock: " + str(producto["stock"])
        if producto["stock"] < STOCK_MINIMO:
            linea = linea + "  <-- STOCK BAJO"
        texto = texto + linea + "\n"
        valor_total = valor_total + producto["precio"] * producto["stock"]
    texto = texto + "Valor total del inventario: " + formatear_dinero(valor_total) + "\n"
    print(texto)
    return texto


def total_vendido() -> float:
    """Suma el total (con IVA) de todas las ventas registradas."""
    total = 0
    for venta in gestor.VENTAS:
        total = total + venta["total"]
    return round(total, 2)


def mas_vendidos(n: int = 3) -> list[tuple[str, int]]:
    """Regresa los n productos mas vendidos como lista de (codigo, unidades)."""
    unidades = {}
    for venta in gestor.VENTAS:
        unidades[venta["codigo"]] = unidades.get(venta["codigo"], 0) + venta["cantidad"]
    # sorted is stable, so ties keep their first-sale order
    ordenados = sorted(unidades.items(), key=lambda par: par[1], reverse=True)
    return ordenados[:n]


def resumen_ventas() -> str:
    """Arma el resumen de ventas del dia, lo imprime y lo regresa."""
    texto = "===== RESUMEN DE VENTAS =====\n"
    for venta in gestor.VENTAS:
        texto = texto + "Folio " + str(venta["folio"]) + ": " + venta["nombre"]
        texto = texto + " x" + str(venta["cantidad"]) + " = " + formatear_dinero(venta["total"]) + "\n"
    texto = texto + "Numero de ventas: " + str(len(gestor.VENTAS)) + "\n"
    texto = texto + "Total del dia: " + formatear_dinero(total_vendido()) + "\n"
    print(texto)
    return texto
