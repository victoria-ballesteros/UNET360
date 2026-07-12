# Seeds — poblado inicial de MongoDB

Coloca aquí un archivo JSON por colección. El script `scripts/seed.py` se ejecuta
al arrancar el contenedor de la API e inserta los documentos **solo si la colección
está vacía** (si ya tiene datos, no la toca).

## Archivos esperados

| Archivo            | Colección en Mongo |
|--------------------|--------------------|
| `location.json`    | `location`         |
| `tag.json`         | `tag`              |
| `node.json`        | `node`             |
| `tentant.json`     | `tentant`          |

> `tenant.json` también se acepta como alias de `tentant.json`.

## Formatos aceptados

- **Array JSON estándar** — exportación de MongoDB Compass (*Export Collection*).
- **Extended JSON / JSONL** — salida de `mongoexport` (soporta `$oid`, `$date`, etc.).

## Cómo exportar desde Atlas

Con Compass conectado al cluster de Atlas: abre cada colección →
*Export Collection* → *Export Full Collection* → formato **JSON**, y guarda el
archivo con el nombre indicado arriba dentro de esta carpeta.

O con `mongoexport`:

```bash
mongoexport --uri "<atlas-uri>" --db catalogs_unet --collection node    --out node.json
mongoexport --uri "<atlas-uri>" --db catalogs_unet --collection location --out location.json
mongoexport --uri "<atlas-uri>" --db catalogs_unet --collection tag      --out tag.json
mongoexport --uri "<atlas-uri>" --db catalogs_unet --collection tentant  --out tentant.json
```
