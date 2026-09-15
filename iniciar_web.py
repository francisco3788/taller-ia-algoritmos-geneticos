# -*- coding: utf-8 -*-
"""Abrir en Spyder y ejecutar: inicia la aplicación web LOCAL sin instalar paquetes.
Detener con el botón rojo de Spyder o Ctrl+C. No cerrar la consola mientras se usa.
"""
import os
import sys
from pathlib import Path
import threading
import webbrowser
from socketserver import ThreadingMixIn
from wsgiref.simple_server import make_server, WSGIServer
# Permite ejecutar desde Spyder aunque su carpeta de trabajo sea otra.
carpeta_proyecto = str(Path(__file__).resolve().parent)
if carpeta_proyecto not in sys.path:
    sys.path.insert(0, carpeta_proyecto)
from app import application


class ServidorLocal(ThreadingMixIn, WSGIServer):
    daemon_threads = True


if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", "8000"))
    direccion = f"http://127.0.0.1:{puerto}/n-reinas"
    print(f"\nTALLER IA · Aplicación web local\nAbre: {direccion}")
    print("Mantén esta consola abierta. Para detener: Ctrl+C o botón rojo de Spyder.")
    print("Este servidor local no está publicado en internet.")
    try:
        with make_server("127.0.0.1", puerto, application, server_class=ServidorLocal) as servidor:
            if os.environ.get("SIN_NAVEGADOR") != "1":
                threading.Timer(0.8, lambda: webbrowser.open(direccion)).start()
            servidor.serve_forever()
    except OSError as e:
        print(f"No se pudo iniciar el puerto {puerto}: {e}")
        print("Detén la ejecución anterior de iniciar_web.py y vuelve a ejecutar.")
    except KeyboardInterrupt:
        print("\nServidor detenido.")
