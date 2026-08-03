# Task Management API

API REST para la gestión de tareas desarrollada con FastAPI.

## Instalación

### 1. Crear contenedores

Requiere tener instalado docker desktop o estar en u entorno Linux

```bash
docker compose up -d
```

La API estará disponible en `http://localhost:8080` -- NOTA: el puerto puerto depoenderá de lao configurado en la variable de entorno API_PORT

## Endpoints

### Documentar todos los endpoints

- `GET /` - Información de la API: Presentación de la API y de sus endpoints principales
- `POST /tasks/` - Crear una nueva tarea: requiere titulo, contenido y fecha de vencimiento. No se permiten titulos duplicados.
- `GET /tasks/{task_id}` - Obtener una tarea por ID. La tarea debe existir
- `PATCH /tasks/{task_id}/completar` - Marcar una tarea como completada. La tarea debe existir
- `GET /tasks/caducadas` - Obtener lista de tareas caducadas: fecha en el pasado y sin completar

Todos los endpoints (salvo el de la raiz) devuelven la tarea afectada (o una lista de tareas si son varias)

## Ejecutar tests

```bash
python test_api.py
```

## Documentación interactiva

Una vez ejecutando la aplicación, puedes acceder a:
- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`

## Detalles de implementacion

Clase TaskManager para gestionar la logica de negocio.

Se ha optado para registrar los datos en un bd Postgre, para cumplir el requisito de comunicar el docker de la API con el de la BBDD.

Se ha utilizado el metodo **set_TaskResponse(self, task_db: Task_db) -> TaskResponse** para centralizar el paso de datos de Task_db a TaskResponse, facilitando la escalabilidad de nuevos campos en la bd
