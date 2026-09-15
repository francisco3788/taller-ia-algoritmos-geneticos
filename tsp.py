# -*- coding: utf-8 -*-
"""Ejercicio 1. Agente viajero: rutas válidas, OX, swap/inversión y elitismo."""
import math
import random
from datos import MATRIZ_DISTANCIAS
from comunes import validar_parametros, torneo
from n_reinas import cruzar_ox


def distancia_ruta(ruta, matriz):
    """Incluye siempre la arista desde la última ciudad hasta la primera."""
    return sum(matriz[ruta[i]][ruta[(i + 1) % len(ruta)]] for i in range(len(ruta)))


def mutar_ruta(ruta, tasa, estrategia, azar):
    hijo = ruta.copy()
    if azar.random() < tasa:
        i, j = sorted(azar.sample(range(len(hijo)), 2))
        if estrategia == "swap":
            hijo[i], hijo[j] = hijo[j], hijo[i]
        else:
            hijo[i:j + 1] = reversed(hijo[i:j + 1])
    return hijo


def resolver_tsp(tam_poblacion=60, tasa_mutacion=0.05,
                 max_generaciones=200, semilla=42, estrategia="inversion", matriz=None):
    validar_parametros(tam_poblacion, tasa_mutacion, max_generaciones, semilla)
    if estrategia not in ("swap", "inversion"):
        raise ValueError("La estrategia debe ser swap o inversion.")
    matriz = MATRIZ_DISTANCIAS if matriz is None else matriz
    n = len(matriz)
    if n < 3 or any(len(fila) != n for fila in matriz):
        raise ValueError("La matriz debe ser cuadrada, con al menos tres ciudades.")
    if any(not isinstance(d, (float, int)) or not math.isfinite(d) or d < 0
           for fila in matriz for d in fila):
        raise ValueError("Las distancias deben ser finitas y no negativas.")
    azar = random.Random(semilla)
    poblacion = [azar.sample(range(n), n) for _ in range(tam_poblacion)]
    mejor_distancia = math.inf
    historial = []
    generacion_mejor = 0
    for generacion in range(max_generaciones + 1):
        distancias = [distancia_ruta(r, matriz) for r in poblacion]
        indice = min(range(tam_poblacion), key=lambda i: distancias[i])
        if distancias[indice] < mejor_distancia - 1e-10:
            mejor_distancia = distancias[indice]
            mejor = poblacion[indice].copy()
            generacion_mejor = generacion
        historial.append({"generacion": generacion, "mejor": mejor_distancia,
                          "promedio": sum(distancias) / tam_poblacion})
        # No se conoce el óptimo: se usa un presupuesto fijo, sin afirmar optimalidad.
        if generacion == max_generaciones:
            break
        nueva = [mejor.copy()]
        while len(nueva) < tam_poblacion:
            p1 = torneo(poblacion, distancias, azar)
            p2 = torneo(poblacion, distancias, azar)
            hijo = cruzar_ox(p1, p2, azar)
            nueva.append(mutar_ruta(hijo, tasa_mutacion, estrategia, azar))
        poblacion = nueva
    # Rotación solo para presentar la ruta iniciando en Ciudad 0.
    pos = mejor.index(0)
    mejor = mejor[pos:] + mejor[:pos]
    return {"n": n, "poblacion": tam_poblacion, "mutacion": tasa_mutacion,
            "estrategia": estrategia, "semilla": semilla,
            "generaciones": generacion, "generacion_mejor": generacion_mejor,
            "ruta": mejor, "ruta_cerrada": mejor + [mejor[0]],
            "distancia": distancia_ruta(mejor, matriz),
            "aptitud": 1 / (distancia_ruta(mejor, matriz) + 1e-9),
            "historial": historial}


if __name__ == "__main__":
    resultado = resolver_tsp()
    print({k: v for k, v in resultado.items() if k != "historial"})
