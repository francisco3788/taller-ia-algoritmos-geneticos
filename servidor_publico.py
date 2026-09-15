# -*- coding: utf-8 -*-
"""Entrada de despliegue público WSGI. Instalar requirements.txt en el servidor."""
import os
from waitress import serve
from app import application

if __name__ == "__main__":
    serve(application, host="0.0.0.0", port=int(os.environ.get("PORT", "8000")),
          threads=4, max_request_body_size=4096)
