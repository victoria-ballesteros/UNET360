# Servicio de Street View de la Universidad Nacional Experimental del Táchira

Implementado con FastAPI, MongoDB y Vue.js

## Requisitos
- Docker (con WSL 2)
- Docker Compose

## Instalación
1. Clonar el repositorio
2. Ejecutar con Docker Compose, individualmente, en las carpeta `unet360` (frontend) y `unet360-api` (backend) (de modo que se tengan los servicios corriendo para ambos sistemas):
```bash
docker compose up --build
```
La API estará disponible en:
- Swagger Docs: http://localhost:8000/docs

El servicio frontend estará disponible en:
- http://localhost/

## Servicios para deploy
1. MongoDB Atlas con imagen de MongoDB para la base de datos.
2. Supabase como bucket para las imágenes.

## Estructura del proyecto (arquitectura hexagonal)
```
unet360-api/
├── adapter/
│   └── database/         # Implementación de MongoDB para cada archivo del folder `entities` (*_repository.py)
├── core/
│   └── entities/         # Modelos de dominio
│   └── service/          # Casos de usuario que utilizan los *_repository.py.
├── docker-compose.yml    # Configuración de Docker
├── Dockerfile            # Dockerfile para el servicio
├── requirements.txt      # Dependencias Python
└── tests/                # Tests unitarios y de integración (TO DO)
```

## Links de interés
- https://cloudinary.com/
- https://render.com/docs/deploy-mongodb
- https://render.com/docs/configure-environment-variables
- https://color.adobe.com/es/create/color-wheel/