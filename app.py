# -*- coding: utf-8 -*-
"""Aplicación WSGI con cuatro interfaces. No necesita Flask ni conexión a internet.

El navegador llama por HTTP a los mismos cuatro módulos Python usados en las pruebas.
Para publicar: servir `app:application` con Waitress, no con el servidor de referencia.
"""
import json
import math
import mimetypes
import threading
from pathlib import Path
from urllib.parse import urlparse
from datos import CIUDADES, MATRIZ_DISTANCIAS, CURSOS, SALAS, FRANJAS, OBJETOS
from n_reinas import resolver_n_reinas
from tsp import resolver_tsp
from salas import resolver_salas
from mochila import resolver_mochila

BASE = Path(__file__).resolve().parent
CUPOS = threading.BoundedSemaphore(2)
PAGINAS = {"/": "n-reinas", "/n-reinas": "n-reinas", "/tsp": "tsp", "/salas": "salas", "/mochila": "mochila"}


def entero(datos, nombre, defecto, minimo, maximo):
    valor = datos.get(nombre, defecto)
    if type(valor) is not int or not minimo <= valor <= maximo:
        raise ValueError(f"{nombre}: se requiere un entero entre {minimo} y {maximo}.")
    return valor


def parametros(datos):
    p = entero(datos, "poblacion", 60, 3, 200)
    g = entero(datos, "generaciones", 200, 0, 1000)
    tasa = datos.get("mutacion", 0.1)
    if type(tasa) not in (int, float) or not math.isfinite(tasa) or not 0 <= tasa <= 1:
        raise ValueError("Mutación: utiliza una probabilidad entre 0 y 1.")
    s = datos.get("semilla", 42)
    if s is not None and (type(s) is not int or abs(s) > 2147483647):
        raise ValueError("Semilla: entero de 32 bits o campo vacío.")
    if p * (g + 1) > 100000:
        raise ValueError("Reduce población o generaciones: el presupuesto web máximo es 100 000 candidatos.")
    return p, tasa, g, s


def resolver(problema, d):
    p, t, g, s = parametros(d)
    if problema == "n-reinas":
        n = entero(d, "n", 6, 6, 8)
        if n not in (6, 8):
            raise ValueError("Para este taller usa N = 6 u 8.")
        return resolver_n_reinas(n, p, t, g, s)
    if problema == "tsp":
        return resolver_tsp(p, t, g, s, d.get("estrategia", "inversion"))
    if problema == "salas":
        elite = d.get("elitismo", True)
        if type(elite) is not bool:
            raise ValueError("Elitismo debe ser verdadero o falso.")
        return resolver_salas(p, t, g, s, elite)
    if problema == "mochila":
        c = entero(d, "capacidad", 35, 1, 120)
        return resolver_mochila(c, d.get("metodo", "penalizacion"), p, t, g, s)
    raise ValueError("Problema desconocido.")


def application(environ, start_response):
    def respuesta(status, cuerpo, tipo="application/json; charset=utf-8"):
        if not isinstance(cuerpo, bytes):
            cuerpo = json.dumps(cuerpo, ensure_ascii=False, allow_nan=False).encode("utf-8")
        start_response(status, [("Content-Type", tipo), ("Content-Length", str(len(cuerpo))),
                               ("X-Content-Type-Options", "nosniff"),
                               ("Cache-Control", "no-store"),
                               ("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-ancestors 'none'")])
        return [cuerpo]

    path = environ.get("PATH_INFO", "/")
    metodo = environ.get("REQUEST_METHOD", "GET")
    try:
        if metodo == "GET" and path in PAGINAS:
            contenido = (BASE / "templates" / f"{PAGINAS[path]}.html").read_bytes()
            return respuesta("200 OK", contenido, "text/html; charset=utf-8")
        if metodo == "GET" and path.startswith("/static/"):
            archivo = (BASE / path.lstrip("/")).resolve()
            if not archivo.is_relative_to((BASE / "static").resolve()) or not archivo.is_file():
                return respuesta("404 Not Found", {"error": "Archivo no encontrado."})
            tipo = mimetypes.guess_type(archivo.name)[0] or "application/octet-stream"
            return respuesta("200 OK", archivo.read_bytes(), tipo + "; charset=utf-8")
        if metodo == "GET" and path == "/api/datos":
            return respuesta("200 OK", {"ciudades": CIUDADES, "matriz": MATRIZ_DISTANCIAS,
                                         "cursos": CURSOS, "salas": SALAS, "franjas": FRANJAS, "objetos": OBJETOS})
        if metodo == "GET" and path == "/health":
            return respuesta("200 OK", {"estado": "activo"})
        if metodo == "POST" and path.startswith("/api/resolver/"):
            if not environ.get("CONTENT_TYPE", "").startswith("application/json"):
                return respuesta("415 Unsupported Media Type", {"error": "Se requiere JSON."})
            origin = environ.get("HTTP_ORIGIN")
            if origin and urlparse(origin).netloc != environ.get("HTTP_HOST"):
                return respuesta("403 Forbidden", {"error": "Origen no permitido."})
            largo = int(environ.get("CONTENT_LENGTH") or 0)
            if not 0 < largo <= 4096:
                return respuesta("400 Bad Request", {"error": "Solicitud vacía o demasiado grande."})
            d = json.loads(environ["wsgi.input"].read(largo))
            if not isinstance(d, dict):
                raise ValueError("Los parámetros deben formar un objeto JSON.")
            if not CUPOS.acquire(blocking=False):
                return respuesta("429 Too Many Requests", {"error": "Hay dos búsquedas en curso. Espera y vuelve a intentar."})
            try:
                r = resolver(path.rsplit("/", 1)[-1], d)
            finally:
                CUPOS.release()
            return respuesta("200 OK", r)
        return respuesta("404 Not Found", {"error": "Recurso no encontrado."})
    except (ValueError, TypeError, json.JSONDecodeError) as e:
        return respuesta("400 Bad Request", {"error": str(e)})
    except Exception:
        import traceback
        traceback.print_exc(file=environ.get("wsgi.errors"))
        return respuesta("500 Internal Server Error", {"error": "No se pudo procesar la solicitud. Revisa la consola del servidor."})
