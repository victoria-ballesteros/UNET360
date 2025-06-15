# Servicio de Street View de la Universidad Nacional Experimental del Táchira

Implementado con FastAPI, MongoDB y Vue.js

## Requisitos
- Docker (con WSL 2)
- Docker Compose
- Python 3.11+

## Instalación
1. Clonar el repositorio
2. Ejecutar con Docker Compose, individualmente, en las carpeta `unet360` (frontend) y `unet360-api` (backend) (de modo que se tengan
los servicios corriendo para ambos sistemas):
```bash
docker compose up --build
```
El servicio backend estará disponible en:
- Swagger Docs: http://localhost:8000/docs

El servicio frontend estará disponible en:
- http://localhost/

## Servicios para deploy
1. Render con imagen de MongoDB para la base de datos.
2. Supabase como bucket para las imágenes.
3. WebService con Render para el backend y para el frontend por separado.

## Links de interés
- https://cloudinary.com/
- https://render.com/docs/deploy-mongodb
- https://render.com/docs/configure-environment-variables
- https://color.adobe.com/es/create/color-wheel/