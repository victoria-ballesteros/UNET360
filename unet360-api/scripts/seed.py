"""Poblado inicial de la base de datos.

Se ejecuta al arrancar el contenedor de la API (ver entrypoint.sh). Para cada
colección busca su archivo JSON dentro de ../seed y, ÚNICAMENTE si la colección
está vacía, inserta los documentos. Si la colección ya tiene datos no se toca,
por lo que es seguro reiniciar el contenedor cuantas veces se quiera.

Formatos de archivo aceptados por colección (../seed/<coleccion>.json):
  - Array JSON estándar        -> exportación de MongoDB Compass
  - Extended JSON / JSONL      -> salida de `mongoexport`
"""

import os
import sys
import time

from bson import json_util
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Directorio con los JSON de las colecciones (../seed respecto a este archivo)
SEED_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "seed")

# Mapeo: nombre de archivo (sin extensión) -> nombre real de la colección.
# "tentant" mantiene el nombre real de la colección (tal cual en el modelo Beanie);
# se acepta "tenant.json" como alias amigable.
FILE_TO_COLLECTION = {
    "location": "location",
    "tag": "tag",
    "node": "node",
    "tentant": "tentant",
    "tenant": "tentant",
}


def log(message):
    print(f"[seed] {message}", flush=True)


def parse_documents(raw):
    """Parsea el contenido de un archivo a una lista de documentos.

    Intenta primero como un único documento/array (Extended JSON). Si falla,
    lo trata como JSONL (un documento por línea).
    """
    raw = raw.strip()
    if not raw:
        return []

    try:
        data = json_util.loads(raw)
        return data if isinstance(data, list) else [data]
    except ValueError:
        documents = []
        for line in raw.splitlines():
            line = line.strip()
            if line:
                documents.append(json_util.loads(line))
        return documents


def wait_for_mongo(uri, retries=30, delay=2):
    """Espera a que MongoDB acepte conexiones antes de sembrar."""
    for attempt in range(1, retries + 1):
        try:
            client = MongoClient(uri, serverSelectionTimeoutMS=2000)
            client.admin.command("ping")
            return client
        except PyMongoError:
            log(f"MongoDB no disponible aún (intento {attempt}/{retries})...")
            time.sleep(delay)
    return None


def main():
    mongo_uri = os.getenv("MONGODB_URL")
    mongo_db_name = os.getenv("MONGODB_DB")

    if not mongo_uri or not mongo_db_name:
        log("MONGODB_URL o MONGODB_DB no están definidos. Se omite el poblado.")
        return 0

    if not os.path.isdir(SEED_DIR):
        log(f"No existe la carpeta de seeds ({SEED_DIR}). Se omite el poblado.")
        return 0

    client = wait_for_mongo(mongo_uri)
    if client is None:
        log("No se pudo conectar a MongoDB. Se omite el poblado.")
        return 0

    database = client.get_database(mongo_db_name)
    log(f"Conectado a la base de datos '{mongo_db_name}'.")

    for file_stem, collection_name in FILE_TO_COLLECTION.items():
        file_path = os.path.join(SEED_DIR, f"{file_stem}.json")
        if not os.path.exists(file_path):
            continue

        collection = database[collection_name]

        # Solo poblar si la colección está vacía (no existe / sin documentos)
        existing = collection.count_documents({})
        if existing > 0:
            log(
                f"Colección '{collection_name}' ya tiene {existing} documento(s); "
                "se omite."
            )
            continue

        with open(file_path, "r", encoding="utf-8") as handle:
            documents = parse_documents(handle.read())

        if not documents:
            log(f"'{file_stem}.json' no contiene documentos; se omite.")
            continue

        collection.insert_many(documents)
        log(
            f"Colección '{collection_name}' poblada con {len(documents)} "
            f"documento(s) desde '{file_stem}.json'."
        )

    client.close()
    log("Poblado inicial finalizado.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:  # noqa: BLE001 - no debe tumbar el arranque
        log(f"Error inesperado durante el poblado: {error}")
        sys.exit(0)
