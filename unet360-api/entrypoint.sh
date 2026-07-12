#!/usr/bin/env bash
# Punto de entrada del contenedor de la API.
# 1. Ejecuta el poblado inicial de la BD (solo siembra colecciones vacías).
# 2. Arranca el proceso indicado por CMD (uvicorn).
set -e

echo "[entrypoint] Verificando poblado inicial de la base de datos..."
python scripts/seed.py || echo "[entrypoint] El poblado falló; se continúa con el arranque."

echo "[entrypoint] Iniciando la aplicación..."
exec "$@"
