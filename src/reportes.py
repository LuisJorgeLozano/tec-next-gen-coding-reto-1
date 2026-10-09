# -*- coding: utf-8 -*-
"""Reportes de la tienda: inventario, ventas y mas vendidos."""

import gestor

# Products with stock below this value are flagged as low stock
STOCK_MINIMO = 5


def hacer_cosa(v):
    # le da formato de dinero al numero
    return "$" + str(round(v, 2))


def productos_stock_bajo() -> list:
    """Regresa la lista de productos con stock por debajo del minimo."""
    temp2 = []
    for k in gestor.INVENTARIO:
        if gestor.INVENTARIO[k]["stock"] < STOCK_MINIMO:
            temp2.append(gestor.INVENTARIO[k])
    return temp2


def reporte_inventario() -> str:
    """Arma el reporte del inventario, lo imprime y lo regresa como texto."""
    s = "===== INVENTARIO =====\n"
    aux = 0
    for k in gestor.INVENTARIO:
        p = gestor.INVENTARIO[k]
        linea = p["codigo"] + " | " + p["nombre"] + " | "
        linea = linea + hacer_cosa(p["precio"]) + " | stock: " + str(p["stock"])
        if p["stock"] < STOCK_MINIMO:
            linea = linea + "  <-- STOCK BAJO"
        s = s + linea + "\n"
        aux = aux + p["precio"] * p["stock"]
    s = s + "Valor total del inventario: " + hacer_cosa(aux) + "\n"
    print(s)
    return s


def total_vendido() -> float:
    """Suma el total (con IVA) de todas las ventas registradas."""
    t = 0
    for v in gestor.VENTAS:
        t = t + v["total"]
    return round(t, 2)


def mas_vendidos(n: int = 3) -> list[tuple[str, int]]:
    """Regresa los n productos mas vendidos como lista de (codigo, unidades)."""
    unidades = {}
    for v in gestor.VENTAS:
        unidades[v["codigo"]] = unidades.get(v["codigo"], 0) + v["cantidad"]
    # sorted is stable, so ties keep their first-sale order
    ordenados = sorted(unidades.items(), key=lambda par: par[1], reverse=True)
    return ordenados[:n]


def resumen_ventas() -> str:
    """Arma el resumen de ventas del dia, lo imprime y lo regresa."""
    s = "===== RESUMEN DE VENTAS =====\n"
    for v in gestor.VENTAS:
        s = s + "Folio " + str(v["folio"]) + ": " + v["nombre"]
        s = s + " x" + str(v["cantidad"]) + " = " + hacer_cosa(v["total"]) + "\n"
    s = s + "Numero de ventas: " + str(len(gestor.VENTAS)) + "\n"
    s = s + "Total del dia: " + hacer_cosa(total_vendido()) + "\n"
    print(s)
    return s
