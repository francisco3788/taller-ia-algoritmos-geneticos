# Taller 1 de Inteligencia Artificial — Algoritmos genéticos

Aplicación Python con cuatro interfaces para los problemas del enunciado: N-Reinas, agente viajero (TSP), asignación de cursos a salas y mochila binaria. La web ejecuta los mismos módulos de los algoritmos; no muestra respuestas predeterminadas.

## Estructura

| Archivo o carpeta | Función |
|---|---|
| `n_reinas.py` | Permutaciones, conflictos diagonales, torneo, OX y mutación por intercambio. |
| `tsp.py` | Recorrido cerrado de ocho ciudades, OX y mutación por intercambio o inversión. |
| `salas.py` | Ocho cursos, cuatro salas y cinco franjas; penalizaciones y comparación con/sin elitismo. |
| `mochila.py` | Quince objetos, cromosomas binarios y métodos de penalización o reparación. |
| `comunes.py`, `datos.py` | Validaciones, operadores compartidos y datos didácticos. |
| `app.py` | Aplicación WSGI y API de los cuatro problemas. |
| `templates/`, `static/` | Interfaces, estilos y comunicación con la API. |
| `iniciar_web.py` | Arranque local desde Spyder o consola. |
| `servidor_publico.py` | Arranque con Waitress para el alojamiento web. |

Los datos de ciudades, cursos, salas y objetos son ficticios. El informe y las evidencias de experimentación se entregan por separado en el paquete del taller; no es necesario publicarlos para ejecutar la aplicación.

## Ejecutar localmente

Mantener todos los archivos y carpetas juntos. Abrir `iniciar_web.py` en Spyder y ejecutar el archivo completo, o ejecutar desde la carpeta del proyecto:

```bash
python iniciar_web.py
```

Abrir `http://127.0.0.1:8000/n-reinas`. Mantener el servidor funcionando mientras se usa el navegador. No se necesitan paquetes adicionales para el arranque local.

## Configuración preparada para Render

Crear un servicio **Web Service** separado para este repositorio, después de confirmar el espacio de trabajo y el plan:

| Campo | Valor |
|---|---|
| Branch | `main` |
| Language / Runtime | Python 3 |
| Root Directory | Vacío: los archivos están en la raíz del repositorio. |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python servidor_publico.py` |
| Health Check Path | `/health` |
| Plan propuesto | Free |

El servidor escucha en `0.0.0.0` y utiliza la variable `PORT` del alojamiento. La versión de Python se establece en `.python-version`. La URL pública se obtiene después de crear el servicio y completar satisfactoriamente su despliegue; subir el código a GitHub no publica por sí solo el servidor Python.

Referencias de configuración: https://render.com/docs/web-services y https://render.com/docs/python-version.

## Rutas

- `/n-reinas`
- `/tsp`
- `/salas`
- `/mochila`
- `/health`: comprobación del estado del servidor.

## Interpretación de resultados

La generación 0 es la población inicial. En N-Reinas se detiene la búsqueda al llegar a cero conflictos o alcanzar el límite. En TSP y mochila se muestra la mejor solución encontrada dentro del presupuesto, sin certificar el óptimo global. En salas se distinguen restricciones duras y equilibrio.

La semilla permite repetir una corrida; dejar el campo vacío no elimina el máximo de generaciones. En la web se limita el trabajo por solicitud y el número de búsquedas simultáneas.
