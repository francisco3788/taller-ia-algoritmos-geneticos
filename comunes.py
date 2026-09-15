# -*- coding: utf-8 -*-
"""Validación y operadores compartidos; las funciones no usan la interfaz web."""
import math

def validar_parametros(poblacion, mutacion, generaciones, semilla):
    if type(poblacion) is not int or poblacion < 3:
        raise ValueError("La población debe ser un entero mayor o igual a 3.")
    if type(generaciones) is not int or generaciones < 0:
        raise ValueError("Las generaciones deben ser un entero no negativo.")
    if isinstance(mutacion, bool) or not isinstance(mutacion, (int, float)) or not math.isfinite(mutacion) or not 0 <= mutacion <= 1:
        raise ValueError("La mutación debe estar entre 0 y 1.")
    if semilla is not None and type(semilla) is not int:
        raise ValueError("La semilla debe ser un entero o None.")

def torneo(poblacion, puntuaciones, azar, maximizar=False):
    indices = azar.sample(range(len(poblacion)), 3)
    escoger = max if maximizar else min
    indice = escoger(indices, key=lambda i: puntuaciones[i])
    return poblacion[indice].copy()

def cruce_un_punto(padre1, padre2, azar):
    corte = azar.randrange(1, len(padre1))
    return padre1[:corte] + padre2[corte:]
