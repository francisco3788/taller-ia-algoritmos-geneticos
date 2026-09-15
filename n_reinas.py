# -*- coding: utf-8 -*-
"""N-Reinas: algoritmo genético y pruebas del enunciado.

Representación: permutación de 0 a N-1; índice = columna, valor = fila.
Método elegido: torneo de 3, cruce OX, mutación swap por hijo y 1 élite.
El algoritmo devuelve datos y puede reutilizarse desde una interfaz web.
"""

import csv
import random
from pathlib import Path


# ---------------- CONFIGURACIÓN ----------------
MODO = "individual"       # "individual" o "pruebas".

# Parámetros de una ejecución individual.
N = 6
TAM_POBLACION = 30
TASA_MUTACION = 0.05

# Parámetros comunes: mantenerlos iguales al comparar.
MAX_GENERACIONES = 1000
SEMILLA = 42

# Pruebas: 12 combinaciones, una corrida por combinación.
VALORES_N = [6, 8]
POBLACIONES = [30, 60]    # Tamaños elegidos; el enunciado no fija cifras.
TASAS_MUTACION = [0.05, 0.10, 0.20]
# ------------------------------------------------


def crear_individuo(n: int, azar: random.Random) -> list[int]:
    return azar.sample(range(n), n)


def crear_poblacion(n, cantidad, azar):
    return [crear_individuo(n, azar) for _ in range(cantidad)]


def contar_conflictos(individuo: list[int]) -> int:
    """Cuenta parejas en diagonal; recibe una permutación sin filas repetidas."""
    conflictos = 0
    for i in range(len(individuo)):
        for j in range(i + 1, len(individuo)):
            if abs(i - j) == abs(individuo[i] - individuo[j]):
                conflictos += 1
    return conflictos


def seleccionar_padre(poblacion, azar):
    participantes = azar.sample(poblacion, 3)
    return min(participantes, key=contar_conflictos).copy()


def cruzar_ox(padre1, padre2, azar):
    """Copia un segmento y completa en orden circular sin repetir valores."""
    n = len(padre1)
    inicio, fin = sorted(azar.sample(range(n), 2))
    hijo = [-1] * n
    hijo[inicio:fin + 1] = padre1[inicio:fin + 1]

    posicion = (fin + 1) % n
    for paso in range(n):
        gen = padre2[(fin + 1 + paso) % n]
        if gen not in hijo:
            hijo[posicion] = gen
            posicion = (posicion + 1) % n
    return hijo


def mutar(individuo, tasa_mutacion, azar):
    """Cada hijo puede sufrir UN intercambio de dos posiciones."""
    hijo = individuo.copy()
    if azar.random() < tasa_mutacion:
        i, j = azar.sample(range(len(hijo)), 2)
        hijo[i], hijo[j] = hijo[j], hijo[i]
    return hijo


def resolver_n_reinas(n: int, tam_poblacion: int, tasa_mutacion: float,
                     max_generaciones: int = 1000,
                     semilla: int | None = 42) -> dict:
    """Resuelve una corrida. No imprime ni guarda archivos: devuelve datos."""
    if not all(type(v) is int for v in (n, tam_poblacion, max_generaciones)):
        raise ValueError("N, población y máximo de generaciones deben ser enteros.")
    if n < 4:
        raise ValueError("Esta implementación admite N >= 4; el taller pide 6 y 8.")
    if tam_poblacion < 3:
        raise ValueError("La población debe ser al menos 3 para nuestro torneo.")
    if max_generaciones < 0:
        raise ValueError("El máximo de generaciones no puede ser negativo.")
    if not isinstance(tasa_mutacion, (int, float)) or not 0 <= tasa_mutacion <= 1:
        raise ValueError("La tasa de mutación debe estar entre 0 y 1.")
    if semilla is not None and type(semilla) is not int:
        raise ValueError("La semilla debe ser un entero o None.")

    # Crear el generador aleatorio y la población UNA SOLA VEZ por corrida.
    azar = random.Random(semilla)
    poblacion = crear_poblacion(n, tam_poblacion, azar)
    historial = []

    for generacion in range(max_generaciones + 1):
        poblacion.sort(key=contar_conflictos)
        mejor = poblacion[0].copy()
        conflictos = contar_conflictos(mejor)
        historial.append(conflictos)

        # Generación 0 = población inicial, antes de producir hijos.
        if conflictos == 0 or generacion == max_generaciones:
            break

        nueva_poblacion = [mejor.copy()]  # Elitismo: conservar al mejor.
        while len(nueva_poblacion) < tam_poblacion:
            padre1 = seleccionar_padre(poblacion, azar)
            padre2 = seleccionar_padre(poblacion, azar)
            hijo = cruzar_ox(padre1, padre2, azar)
            hijo = mutar(hijo, tasa_mutacion, azar)
            nueva_poblacion.append(hijo)

        # Reemplazar por los descendientes; NO reiniciar con población aleatoria.
        poblacion = nueva_poblacion

    return {
        "n": n, "poblacion": tam_poblacion, "mutacion": tasa_mutacion,
        "semilla": semilla, "max_generaciones": max_generaciones,
        "generaciones": generacion, "conflictos": conflictos,
        "exito": conflictos == 0, "vector": mejor, "historial": historial
    }


def mostrar_resultado(resultado):
    print("\nRESULTADO FINAL")
    print(f"N: {resultado['n']} | Población: {resultado['poblacion']}")
    print(f"Mutación: {resultado['mutacion']} | Semilla: {resultado['semilla']}")
    print(f"Generaciones realizadas: {resultado['generaciones']}")
    print(f"Mejor vector: {resultado['vector']}")
    print(f"Conflictos: {resultado['conflictos']}")
    if resultado["exito"]:
        print("SOLUCIÓN ENCONTRADA: ninguna pareja de reinas se ataca.")
    else:
        print("LÍMITE ALCANZADO: no se encontró cero conflictos en esta corrida.")


def ejecutar_pruebas():
    """Una corrida por cada combinación: 2 x 2 x 3 = 12."""
    resultados = []
    print("N | Población | Mutación | Generaciones | Conflictos | Éxito | Vector")
    for n in VALORES_N:
        for poblacion in POBLACIONES:
            for tasa in TASAS_MUTACION:
                r = resolver_n_reinas(n, poblacion, tasa, MAX_GENERACIONES, SEMILLA)
                resultados.append(r)
                estado = "SI" if r["exito"] else "NO"
                print(f"{n} | {poblacion:9} | {tasa:8.2f} | "
                      f"{r['generaciones']:12} | {r['conflictos']:9} | "
                      f"{estado:5} | {r['vector']}")
    return resultados


def guardar_resultados(resultados, ruta: Path):
    """Guarda la tabla de pruebas como evidencia para el informe."""
    columnas = ["n", "poblacion", "mutacion", "semilla", "max_generaciones",
                "generaciones", "conflictos", "exito", "vector"]
    with ruta.open("w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas, delimiter=";")
        escritor.writeheader()
        for r in resultados:
            fila = {columna: r[columna] for columna in columnas}
            fila["exito"] = "SI" if r["exito"] else "NO"
            fila["mutacion"] = f"{r['mutacion']:.2f}".replace(".", ",")
            escritor.writerow(fila)


# Solo se ejecuta al abrir este archivo como programa, no al importarlo en la web.
if __name__ == "__main__":
    if MODO == "individual":
        resultado = resolver_n_reinas(
            N, TAM_POBLACION, TASA_MUTACION, MAX_GENERACIONES, SEMILLA)
        print("EVOLUCIÓN: conflictos del mejor individuo")
        for generacion, conflictos in enumerate(resultado["historial"]):
            print(f"Generación {generacion}: {conflictos} conflictos")
        mostrar_resultado(resultado)

    elif MODO == "pruebas":
        resultados = ejecutar_pruebas()
        carpeta = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
        ruta = carpeta / "resultados_n_reinas.csv"
        try:
            guardar_resultados(resultados, ruta)
            print(f"\nTabla de pruebas guardada en: {ruta}")
        except OSError as error:
            print(f"No se pudo guardar el CSV: {error}")
            print("Los resultados siguen visibles en la consola.")
    else:
        raise ValueError('MODO debe ser "individual" o "pruebas".')
