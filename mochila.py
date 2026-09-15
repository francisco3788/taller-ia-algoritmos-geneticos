# -*- coding: utf-8 -*-
"""Ejercicio 3. Mochila binaria: comparar penalización con reparación."""
import random
from datos import OBJETOS
from comunes import validar_parametros, torneo, cruce_un_punto


def peso_valor(individuo):
    return (sum(o["peso"] * bit for o, bit in zip(OBJETOS, individuo)),
            sum(o["valor"] * bit for o, bit in zip(OBJETOS, individuo)))


def reparar(individuo, capacidad):
    """Retira objetos de menor relación valor/peso hasta respetar la capacidad."""
    hijo = individuo.copy()
    peso, _ = peso_valor(hijo)
    seleccionados = sorted((i for i, b in enumerate(hijo) if b),
                           key=lambda i: (OBJETOS[i]["valor"] / OBJETOS[i]["peso"], i))
    for i in seleccionados:
        if peso <= capacidad:
            break
        hijo[i] = 0
        peso -= OBJETOS[i]["peso"]
    return hijo


def evaluar_mochila(individuo, capacidad):
    peso, valor = peso_valor(individuo)
    exceso = max(0, peso - capacidad)
    coeficiente = 1 + sum(o["valor"] for o in OBJETOS)
    # Con pesos/capacidades enteros, todo inválido tiene puntuación negativa.
    return {"peso": peso, "valor": valor, "exceso": exceso,
            "aptitud": valor - coeficiente * exceso, "valido": exceso == 0}


def resolver_mochila(capacidad=35, metodo="penalizacion", tam_poblacion=60,
                     tasa_mutacion=0.10, max_generaciones=200, semilla=42):
    validar_parametros(tam_poblacion, tasa_mutacion, max_generaciones, semilla)
    if type(capacidad) is not int or capacidad <= 0:
        raise ValueError("La capacidad debe ser un entero positivo.")
    if metodo not in ("penalizacion", "reparacion"):
        raise ValueError("Método: penalizacion o reparacion.")
    azar = random.Random(semilla)
    poblacion = [[azar.randrange(2) for _ in OBJETOS] for _ in range(tam_poblacion)]
    # La misma referencia factible inicial para ambos métodos.
    poblacion[0] = [0] * len(OBJETOS)
    if metodo == "reparacion":
        poblacion = [reparar(ind, capacidad) for ind in poblacion]
    mejor_clave = (-float("inf"), 0)
    historial = []
    generacion_mejor = 0
    for generacion in range(max_generaciones + 1):
        evaluaciones = [evaluar_mochila(ind, capacidad) for ind in poblacion]
        claves = [(e["aptitud"], -e["peso"]) for e in evaluaciones]
        indice = max(range(tam_poblacion), key=lambda i: claves[i])
        if claves[indice] > mejor_clave:
            mejor_clave = claves[indice]
            mejor = poblacion[indice].copy()
            generacion_mejor = generacion
        e = evaluar_mochila(mejor, capacidad)
        historial.append({"generacion": generacion, "mejor": e["valor"], "peso": e["peso"]})
        if generacion == max_generaciones:
            break
        nueva = [mejor.copy()]
        while len(nueva) < tam_poblacion:
            p1 = torneo(poblacion, claves, azar, maximizar=True)
            p2 = torneo(poblacion, claves, azar, maximizar=True)
            hijo = cruce_un_punto(p1, p2, azar)
            if azar.random() < tasa_mutacion:
                i = azar.randrange(len(OBJETOS))
                hijo[i] = 1 - hijo[i]
            if metodo == "reparacion":
                hijo = reparar(hijo, capacidad)
            nueva.append(hijo)
        poblacion = nueva
    return {"capacidad": capacidad, "metodo": metodo, "poblacion": tam_poblacion,
            "mutacion": tasa_mutacion, "semilla": semilla, "generaciones": generacion,
            "generacion_mejor": generacion_mejor, "vector": mejor,
            "seleccionados": [o["id"] for o, b in zip(OBJETOS, mejor) if b],
            **evaluar_mochila(mejor, capacidad), "historial": historial}


if __name__ == "__main__":
    resultado = resolver_mochila()
    print({k: v for k, v in resultado.items() if k != "historial"})
