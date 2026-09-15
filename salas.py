# -*- coding: utf-8 -*-
"""Ejercicio 2. Cursos/salas: penalización de restricciones y equilibrio."""
from collections import Counter
import random
from datos import CURSOS, SALAS, FRANJAS
from comunes import validar_parametros, torneo, cruce_un_punto


def minimo_cuadrados(total, grupos):
    q, r = divmod(total, grupos)
    return r * (q + 1) ** 2 + (grupos - r) * q ** 2


def evaluar_horario(individuo):
    """Cada gen es (índice_sala, índice_franja) para el curso de ese índice."""
    desglose = {"sobrecupo": 0, "computadores_faltantes": 0, "software_faltante": 0,
                "choques": 0, "franja_curso": 0, "bloqueo_sala": 0}
    ocupacion = Counter(individuo)
    desglose["choques"] = sum(c * (c - 1) // 2 for c in ocupacion.values())
    for curso, (s, f) in zip(CURSOS, individuo):
        sala = SALAS[s]
        desglose["sobrecupo"] += max(0, curso["estudiantes"] - sala["capacidad"])
        desglose["computadores_faltantes"] += max(0, curso["estudiantes"] - sala["computadores"])
        desglose["software_faltante"] += len(set(curso["software"]) - set(sala["software"]))
        desglose["franja_curso"] += int(f not in curso["permitidas"])
        desglose["bloqueo_sala"] += int(f in sala["bloqueadas"])
    cargas_salas = [sum(s == j for s, f in individuo) for j in range(len(SALAS))]
    cargas_franjas = [sum(f == j for s, f in individuo) for j in range(len(FRANJAS))]
    n = len(CURSOS)
    equilibrio = (sum(c*c for c in cargas_salas) - minimo_cuadrados(n, len(SALAS))
                  + sum(c*c for c in cargas_franjas) - minimo_cuadrados(n, len(FRANJAS)))
    duras = sum(desglose.values())
    # Para 8 cursos, equilibrio <= 98: 1000 garantiza prioridad a restricciones duras.
    return {"duras": duras, "equilibrio": equilibrio,
            "penalizacion": 1000 * duras + equilibrio, "valido": duras == 0,
            "desglose": desglose, "cargas_salas": cargas_salas,
            "cargas_franjas": cargas_franjas}


def resolver_salas(tam_poblacion=80, tasa_mutacion=0.20,
                   max_generaciones=400, semilla=42, elitismo=True):
    validar_parametros(tam_poblacion, tasa_mutacion, max_generaciones, semilla)
    if type(elitismo) is not bool:
        raise ValueError("Elitismo debe ser True o False.")
    azar = random.Random(semilla)
    nuevo_gen = lambda: (azar.randrange(len(SALAS)), azar.randrange(len(FRANJAS)))
    poblacion = [[nuevo_gen() for _ in CURSOS] for _ in range(tam_poblacion)]
    historial = []
    mejor_p = float("inf")
    generacion_mejor = 0
    primera_valida = None
    retrocesos = 0
    anterior = float("inf")
    for generacion in range(max_generaciones + 1):
        evaluaciones = [evaluar_horario(ind) for ind in poblacion]
        puntos = [e["penalizacion"] for e in evaluaciones]
        indice = min(range(tam_poblacion), key=lambda i: puntos[i])
        actual = puntos[indice]
        if actual > anterior:
            retrocesos += 1
        anterior = actual
        if actual < mejor_p:
            mejor_p = actual
            mejor = poblacion[indice].copy()
            generacion_mejor = generacion
        if primera_valida is None and any(e["valido"] for e in evaluaciones):
            primera_valida = generacion
        historial.append({"generacion": generacion, "mejor": mejor_p,
                          "mejor_poblacion": actual,
                          "duras": evaluar_horario(mejor)["duras"]})
        if mejor_p == 0 or generacion == max_generaciones:
            break
        # El archivo histórico NO se reintroduce cuando elitismo=False.
        nueva = [poblacion[indice].copy()] if elitismo else []
        while len(nueva) < tam_poblacion:
            p1 = torneo(poblacion, puntos, azar)
            p2 = torneo(poblacion, puntos, azar)
            hijo = cruce_un_punto(p1, p2, azar)
            if azar.random() < tasa_mutacion:
                hijo[azar.randrange(len(CURSOS))] = nuevo_gen()
            nueva.append(hijo)
        poblacion = nueva
    evaluacion = evaluar_horario(mejor)
    horario = [{"curso": c["id"], "nombre": c["nombre"], "estudiantes": c["estudiantes"],
                "sala": SALAS[s]["id"], "franja": f, "hora": FRANJAS[f]}
               for c, (s, f) in zip(CURSOS, mejor)]
    return {"poblacion": tam_poblacion, "mutacion": tasa_mutacion, "semilla": semilla,
            "elitismo": elitismo, "generaciones": generacion,
            "generacion_mejor": generacion_mejor, "primera_valida": primera_valida,
            "retrocesos": retrocesos, "penalizacion_final_poblacion": actual,
            "vector": mejor, "horario": horario, **evaluacion, "historial": historial}


if __name__ == "__main__":
    resultado = resolver_salas()
    print({k: v for k, v in resultado.items() if k != "historial"})
