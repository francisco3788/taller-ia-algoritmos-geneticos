# -*- coding: utf-8 -*-
"""Datos didácticos diseñados para el taller; no corresponden a instituciones reales."""
from math import hypot

# Ocho ciudades ficticias. Coordenadas y distancias en unidades de distancia (u.d.).
CIUDADES = [
    {"id": i, "nombre": f"Ciudad {i}", "x": x, "y": y}
    for i, (x, y) in enumerate([(0, 0), (2, 7), (5, 3), (8, 8),
                               (11, 1), (13, 6), (6, 12), (15, 12)])
]
MATRIZ_DISTANCIAS = [[hypot(a["x"]-b["x"], a["y"]-b["y"])
                       for b in CIUDADES] for a in CIUDADES]
FRANJAS = ["F1 · 07:00–09:00", "F2 · 09:00–11:00", "F3 · 11:00–13:00",
           "F4 · 14:00–16:00", "F5 · 16:00–18:00"]
SALAS = [
    {"id": "S1", "capacidad": 30, "computadores": 30,
     "software": ["Python", "SQL"], "bloqueadas": [4]},
    {"id": "S2", "capacidad": 25, "computadores": 25,
     "software": ["Python", "R"], "bloqueadas": [0]},
    {"id": "S3", "capacidad": 40, "computadores": 40,
     "software": ["Python", "SQL", "CAD"], "bloqueadas": [3]},
    {"id": "S4", "capacidad": 20, "computadores": 20,
     "software": ["Python", "R", "Redes"], "bloqueadas": [2]},
]
CURSOS = [
    {"id": "C1", "nombre": "Programación", "estudiantes": 28,
     "software": ["Python"], "permitidas": [0, 1, 2, 3]},
    {"id": "C2", "nombre": "Bases de datos", "estudiantes": 32,
     "software": ["SQL"], "permitidas": [0, 1, 3]},
    {"id": "C3", "nombre": "Estadística", "estudiantes": 22,
     "software": ["R"], "permitidas": [1, 2, 3, 4]},
    {"id": "C4", "nombre": "Diseño CAD", "estudiantes": 36,
     "software": ["CAD"], "permitidas": [0, 2, 4]},
    {"id": "C5", "nombre": "Redes", "estudiantes": 18,
     "software": ["Redes"], "permitidas": [0, 1, 2, 4]},
    {"id": "C6", "nombre": "Inteligencia artificial", "estudiantes": 24,
     "software": ["Python"], "permitidas": [1, 2, 3]},
    {"id": "C7", "nombre": "Análisis de datos", "estudiantes": 20,
     "software": ["R"], "permitidas": [0, 2, 3, 4]},
    {"id": "C8", "nombre": "Desarrollo web", "estudiantes": 26,
     "software": ["Python"], "permitidas": [0, 1, 2, 3, 4]},
]
# Cada curso necesita un computador por estudiante. Franjas de una jornada tipo.
# Pesos y valores son enteros ficticios en unidades de peso (u.p.) y valor (u.v.).
OBJETOS = [
    {"id": f"O{i+1:02}", "peso": p, "valor": v}
    for i, (p, v) in enumerate([(2, 12), (3, 20), (5, 25), (7, 35), (8, 39),
                                (9, 42), (4, 23), (6, 31), (15, 70), (10, 44),
                                (11, 50), (1, 8), (12, 54), (13, 56), (14, 65)])
]
CAPACIDADES = [35, 50]
