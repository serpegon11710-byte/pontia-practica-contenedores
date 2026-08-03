import requests
import json
from datetime import datetime, date, timedelta

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Carga las variables del archivo .env al entorno de ejecución
load_dotenv()

# Añade la carpeta 'python-api/src' al PYTHONPATH de forma dinámica
current_dir = Path(__file__).resolve().parent
src_path = current_dir.parent.parent /  "src"
sys.path.append(str(src_path))

from models import TaskResponse

def get_port():
    return int(os.getenv("API_PORT", 8080))

def get_base_url():
    return "http://127.0.0.1:{port}".format(port=get_port())


def get_database_url():

     return f"postgresql+psycopg2://{os.getenv('DATABASE_USER', 'none')}:{os.getenv('DATABASE_PASSWORD', 'none')}@{os.getenv('DATABASE_SERVER', 'none')}:{os.getenv('DATABASE_PORT', 'none')}/{os.getenv('DATABASE_CATALOG', 'none')}"
#    return f"postgresql+psycopg2://{os.getenv('DATABASE_USER', 'fastapi_user')}:{os.getenv('DATABASE_PASSWORD', 'secret123')}@{os.getenv('DATABASE_SERVER', 'localhost')}:{os.getenv('DATABASE_PORT', 5432)}/{os.getenv('DATABASE_CATALOG', 'users')}"

request_timeout = 10  # Tiempo de espera en segundos para las solicitudes HTTP

def format_timestamp(timestamp: str) -> str:
    """Formatea un timestamp en formato ISO 8601 a una cadena legible"""
    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return timestamp  # Devuelve el timestamp original si no se puede formatear

def test_creacion_tarea():

    print(f"Paso 1: Creacion de tarea")
    url_test_create = get_base_url() + "/tasks/"
    titulo= "Tarea de prueba - " + str(datetime.now())
    task_data={
        "titulo": titulo,
        "contenido": "Contenido de la tarea de prueba 'test_crear_tarea'",
        "deadline": (date.today() + timedelta(days=1)).isoformat()
    }

    response_created  = requests.post(url_test_create, json=task_data, timeout=request_timeout)
    print (f"Respuesta: {response_created.json()} Tarea_nueva: {task_data}")
    
    assert response_created.status_code == 201, f"Codigo de respuesta tarea creada incorrecto {response_created.status_code}. Se esperaba 201"
    assert response_created.json()["titulo"] == task_data["titulo"], f"El titulo de la tare creada no coincide ({task_data['titulo']} || {response_created.json()['titulo']})"
    assert response_created.json()["contenido"] == task_data["contenido"], f"El contenido de la tarea creada no coincide ({task_data['contenido']} || {response_created.json()['contenido']})"
    assert response_created.json()["deadline"] == task_data["deadline"], f"La fecha de vencimiento de la tarea creada no coincide ({str(task_data['deadline'])} || {response_created.json()['deadline']})"
    assert response_created.json()["completada"] == False, f"La tarea creada no debería estar completada al crearla ({response_created.json()['completada']})"
    assert "fecha_creacion" in response_created.json(), "La respuesta creada no contiene la fecha de creación"
    assert "id" in response_created.json(), "La respuesta creada no contiene el ID de la tarea"
    assert "fecha_modificacion" in response_created.json(), "La respuesta creada no contiene la fecha de modificación"

    print (f"Tarea creada exitosamente.")
    print ("Paso 1 completado con éxito")
    print ()

    print (f"Paso 2: Verificacion de obtener tarea contra tarea creada")
    task_id = response_created.json()["id"]    
    task_created=TaskResponse(**response_created.json())
    url_test_fetch = get_base_url() + f"/tasks/{task_id}"
    response_fetched  = requests.get(url_test_fetch, timeout=request_timeout)
    print (f"Respuesta: {response_fetched.json()} Tarea_nueva: {task_created}")
    assert response_fetched.status_code == 200, f"Codigo de respuesta tarea obtenida incorrecto {response_fetched.status_code}. Se esperaba 200"
    assert task_created.titulo == response_fetched.json()["titulo"], f"El titulo de la tarea obtenida no coincide con la tarea creada ({response_fetched.json()['titulo']} || {task_created.titulo})"
    assert task_created.contenido == response_fetched.json()["contenido"], f"El contenido de la tarea obtenida no coincide con la tarea creada ({response_fetched.json()['contenido']} || {task_created.contenido})"
    assert format_timestamp(str(task_created.deadline)) == format_timestamp(str(response_fetched.json()["deadline"])), f"La fecha de vencimiento de la tarea obtenida no coincide con la tarea creada ({format_timestamp(str(response_fetched.json()['deadline']))} || {format_timestamp(str(task_created.deadline))})"
    assert task_created.completada == response_fetched.json()["completada"], f"El estado de completado de la tarea obtenida no coincide con la tarea creada ({response_fetched.json()['completada']} || {task_created.completada})"
    assert format_timestamp(str(task_created.fecha_creacion)) == format_timestamp(str(response_fetched.json()["fecha_creacion"])), f"La fecha de creación de la tarea obtenida no coincide con la tarea creada ({format_timestamp(response_fetched.json()['fecha_creacion'])} || {format_timestamp(str(task_created.fecha_creacion))})"
    assert (format_timestamp(str(task_created.fecha_modificacion)) == format_timestamp(str(response_fetched.json()["fecha_modificacion"])) or (task_created.fecha_modificacion is None and response_fetched.json()["fecha_modificacion"] is None)), f"La fecha de modificación de la tarea obtenida no coincide con la tarea creada ({format_timestamp(str(response_fetched.json()['fecha_modificacion']))} || {format_timestamp(str(task_created.fecha_modificacion))})"
    print (f"Tarea obtenida exitosamente.")
    print ("Paso 2 completado con éxito")
    print ()

    print (f"Paso 3: Verificacion de obtener tarea contra datos iniciales")
    print (f"Respuesta: {response_fetched.json()} Tarea_nueva: {task_data}")
    assert response_fetched.json()["titulo"] == task_data["titulo"], f"El titulo de la tarea obtenida no coincide ({task_data['titulo']} || {response_fetched.json()['titulo']})"
    assert response_fetched.json()["contenido"] == task_data["contenido"], f"El contenido de la tarea obtenida no coincide ({task_data['contenido']} || {response_fetched.json()['contenido']})"
    assert response_fetched.json()["deadline"] == task_data["deadline"], f"La fecha de vencimiento de la tarea obtenida no coincide ({str(task_data['deadline'])} || {response_fetched.json()['deadline']})"
    assert response_fetched.json()["completada"] == False, f"La tarea obtenida no debería estar completada al crearla ({response_fetched.json()['completada']})"
    assert "fecha_creacion" in response_fetched.json(), "La respuesta obtenida no contiene la fecha de creación"
    assert "id" in response_fetched.json(), "La respuesta obtenida no contiene el ID de la tarea"
    assert "fecha_modificacion" in response_fetched.json(), "La respuesta obtenida no contiene la fecha de modificación"
    print (f"Tarea obtenida exitosamente.")
    print ("Paso 3 completado con éxito")
    print ()

    print ("Paso 4: Validar titulo duplicado")
    response_duplicate  = requests.post(url_test_create, json=task_data, timeout=request_timeout)    
    print (f"Respuesta: {response_duplicate.json()} Tarea_nueva: {task_data}")
    assert response_duplicate.status_code == 400, f"Creando tarea existente, codigo de respuesta incorrecto {response_duplicate.status_code}. Se esperaba 400"
    print ("Paso 4 completado con éxito")
    print ()

    print ("Paso 5: Completar tarea")
    url_test_complete = get_base_url() + f"/tasks/{task_id}/completar"
    response_complete  = requests.patch(url_test_complete, timeout=request_timeout)
    print (f"Respuesta: {response_complete.json()} URL: {url_test_complete}")
    assert response_complete.status_code == 200, f"Codigo de respuesta incorrecto {response_complete.status_code}. Se esperaba 200"
    assert response_complete.json()["completada"] == True, f"La tarea no se ha marcado como completada ({response_complete.json()['completada']})"
    assert response_complete.json()["id"] == task_id, f"El ID de la tarea no coincide ({response_complete.json()['id']} || {task_id})"
    print ("Paso 5 completado con éxito")
    print()

    print ("Paso 6: Recuperar tarea completada")
    response_fetched_complete  = requests.get(url_test_fetch, timeout=request_timeout)
    print (f"Respuesta: {response_fetched_complete.json()}")
    assert response_fetched_complete.status_code == 200, f"Codigo de respuesta tarea obtenida incorrecto {response_fetched_complete.status_code}. Se esperaba 200"
    assert task_created.titulo == response_fetched_complete.json()["titulo"], f"El titulo de la tarea obtenida no coincide con la tarea creada ({response_fetched_complete.json()['titulo']} || {task_created.titulo})"
    assert task_created.contenido == response_fetched_complete.json()["contenido"], f"El contenido de la tarea obtenida no coincide con la tarea creada ({response_fetched_complete.json()['contenido']} || {task_created.contenido})"
    assert format_timestamp(str(task_created.deadline)) == format_timestamp(str(response_fetched_complete.json()["deadline"])), f"La fecha de vencimiento de la tarea obtenida no coincide con la tarea creada ({format_timestamp(str(response_fetched_complete.json()['deadline']))} || {format_timestamp(str(task_created.deadline))})"
    assert response_fetched_complete.json()["completada"] == True, f"El estado de completado de la tarea obtenida no está completada ({response_fetched_complete.json()['completada']})"
    assert format_timestamp(str(task_created.fecha_creacion)) == format_timestamp(str(response_fetched_complete.json()["fecha_creacion"])), f"La fecha de creación de la tarea obtenida no coincide con la tarea creada ({format_timestamp(str(response_fetched_complete.json()['fecha_creacion']))} || {format_timestamp(str(task_created.fecha_creacion))})"
    assert (format_timestamp(str(task_created.fecha_modificacion)) is not None), f"La fecha de modificación de la tarea completada no puede estar vacía({format_timestamp(str(response_fetched_complete.json()['fecha_modificacion']))}"
    print (f"Tarea obtenida exitosamente.")
    print ("Paso 6 completado con éxito")
    print ()
    pass

def test_tareas_caducadas():

    print(f"Paso 1: Creacion de tarea")
    url_test_create = get_base_url() + "/tasks/"
    titulo= "Tarea de prueba - " + str(datetime.now())
    task_data={
        "titulo": titulo,
        "contenido": "Contenido de la tarea de prueba 'test_crear_tarea'",
        "deadline": (date.today() + timedelta(days=-1)).isoformat()
    }

    response_created  = requests.post(url_test_create, json=task_data, timeout=request_timeout)
    print (f"Respuesta: {response_created.json()} Tarea_nueva: {task_data}")
    
    assert response_created.status_code == 201, f"Codigo de respuesta tarea creada incorrecto {response_created.status_code}. Se esperaba 201"
    assert response_created.json()["titulo"] == task_data["titulo"], f"El titulo de la tare creada no coincide ({task_data['titulo']} || {response_created.json()['titulo']})"
    assert response_created.json()["contenido"] == task_data["contenido"], f"El contenido de la tarea creada no coincide ({task_data['contenido']} || {response_created.json()['contenido']})"
    assert response_created.json()["deadline"] == task_data["deadline"], f"La fecha de vencimiento de la tarea creada no coincide ({str(task_data['deadline'])} || {response_created.json()['deadline']})"
    assert response_created.json()["completada"] == False, f"La tarea creada no debería estar completada al crearla ({response_created.json()['completada']})"
    assert response_created.json()["deadline"] < date.today().isoformat(), f"La tarea creada no está caducada ({response_created.json()['deadline']} || {date.today().isoformat()})"
    assert "fecha_creacion" in response_created.json(), "La respuesta creada no contiene la fecha de creación"
    assert "id" in response_created.json(), "La respuesta creada no contiene el ID de la tarea"
    assert "fecha_modificacion" in response_created.json(), "La respuesta creada no contiene la fecha de modificación"

    print (f"Tarea creada exitosamente.")
    print ("Paso 1 completado con éxito")
    print ()

    print (f"Paso 2: Verificacion de obtener tarea contra tarea creada")
    task_id = response_created.json()["id"]    
    task_created=TaskResponse(**response_created.json())
    url_test_fetch = get_base_url() + f"/tasks/{task_id}"
    response_fetched  = requests.get(url_test_fetch, timeout=request_timeout)
    print (f"Respuesta: {response_fetched.json()} Tarea_nueva: {task_created}")
    assert response_fetched.status_code == 200, f"Codigo de respuesta tarea obtenida incorrecto {response_fetched.status_code}. Se esperaba 200"
    assert task_created.titulo == response_fetched.json()["titulo"], f"El titulo de la tarea obtenida no coincide con la tarea creada ({response_fetched.json()['titulo']} || {task_created.titulo})"
    assert task_created.contenido == response_fetched.json()["contenido"], f"El contenido de la tarea obtenida no coincide con la tarea creada ({response_fetched.json()['contenido']} || {task_created.contenido})"
    assert format_timestamp(str(task_created.deadline)) == format_timestamp(str(response_fetched.json()["deadline"])), f"La fecha de vencimiento de la tarea obtenida no coincide con la tarea creada ({format_timestamp(str(response_fetched.json()['deadline']))} || {format_timestamp(str(task_created.deadline))})"
    assert task_created.completada == response_fetched.json()["completada"], f"El estado de completado de la tarea obtenida no coincide con la tarea creada ({response_fetched.json()['completada']} || {task_created.completada})"
    assert format_timestamp(str(task_created.fecha_creacion)) == format_timestamp(str(response_fetched.json()["fecha_creacion"])), f"La fecha de creación de la tarea obtenida no coincide con la tarea creada ({format_timestamp(response_fetched.json()['fecha_creacion'])} || {format_timestamp(str(task_created.fecha_creacion))})"
    assert (format_timestamp(str(task_created.fecha_modificacion)) == format_timestamp(str(response_fetched.json()["fecha_modificacion"])) or (task_created.fecha_modificacion is None and response_fetched.json()["fecha_modificacion"] is None)), f"La fecha de modificación de la tarea obtenida no coincide con la tarea creada ({format_timestamp(str(response_fetched.json()['fecha_modificacion']))} || {format_timestamp(str(task_created.fecha_modificacion))})"
    print (f"Tarea obtenida exitosamente.")
    print ("Paso 2 completado con éxito")
    print ()

    print (f"Paso 3: Verificacion de obtener tarea contra datos iniciales")
    print (f"Respuesta: {response_fetched.json()} Tarea_nueva: {task_data}")
    assert response_fetched.json()["titulo"] == task_data["titulo"], f"El titulo de la tarea obtenida no coincide ({task_data['titulo']} || {response_fetched.json()['titulo']})"
    assert response_fetched.json()["contenido"] == task_data["contenido"], f"El contenido de la tarea obtenida no coincide ({task_data['contenido']} || {response_fetched.json()['contenido']})"
    assert response_fetched.json()["deadline"] == task_data["deadline"], f"La fecha de vencimiento de la tarea obtenida no coincide ({str(task_data['deadline'])} || {response_fetched.json()['deadline']})"
    assert response_fetched.json()["completada"] == False, f"La tarea obtenida no debería estar completada al crearla ({response_fetched.json()['completada']})"
    assert "fecha_creacion" in response_fetched.json(), "La respuesta obtenida no contiene la fecha de creación"
    assert "id" in response_fetched.json(), "La respuesta obtenida no contiene el ID de la tarea"
    assert "fecha_modificacion" in response_fetched.json(), "La respuesta obtenida no contiene la fecha de modificación"
    print (f"Tarea obtenida exitosamente.")
    print ("Paso 3 completado con éxito")
    print ()

    print ("Paso 4: Recuperar tareas caducadas")
    url_test_expired = get_base_url() + f"/tasks/caducadas"
    response_expired  = requests.get(url_test_expired, timeout=request_timeout)
    print (f"Respuesta: {response_expired.json()} URL: {url_test_expired}")
    assert response_expired.status_code == 200, f"Codigo de respuesta incorrecto {response_expired.status_code}. Se esperaba 200"
    assert response_expired.json() is not None and len(response_expired.json()) > 0, "No se han encontrado tareas caducadas en la respuesta"
    assert any(task["id"] == task_id for task in response_expired.json()), f"No se encontró la tarea caducada recien creada Respuesta: {response_expired.json()} Tarea creada: {task_created}"
    assert all(task["completada"] == False for task in response_expired.json()), f"Se encontró una tarea caducada que está marcada como completada {response_expired.json()}"
    assert all(task["deadline"] < date.today().isoformat() for task in response_expired.json()), f"Se encontró una tarea caducada que no está realmente caducada {response_expired.json()}"
    print ("Paso 4 completado con éxito")
    print()

    print ("Paso 5: Completar tareas")
    for task in response_expired.json():
        task_id = task["id"]
        print (f"Completando tarea caducada con ID: {task_id}")
        url_test_complete_expired = get_base_url() + f"/tasks/{task_id}/completar"
        response_complete_expired  = requests.patch(url_test_complete_expired, timeout=request_timeout)
        assert response_complete_expired.status_code == 200, f"Codigo de respuesta incorrecto {response_complete_expired.status_code}. Se esperaba 200"
        assert response_complete_expired.json()["completada"] == True, f"La tarea no se ha marcado como completada ({response_complete_expired.json()['completada']})"
        assert response_complete_expired.json()["id"] == task_id, f"El ID de la tarea no coincide ({response_complete_expired.json()['id']} || {task_id})"
        url_fecth_complete_expired = get_base_url() + f"/tasks/{task_id}"
        response_fetched_complete_expired  = requests.get(url_fecth_complete_expired, timeout=request_timeout)
        assert response_fetched_complete_expired.status_code == 200, f"Codigo de respuesta tarea obtenida incorrecto {response_fetched_complete_expired.status_code}. Se esperaba 200"
        assert response_fetched_complete_expired.json()["completada"] == True, f"La tarea obtenida no está marcada como completada ({response_fetched_complete_expired.json()['completada']})"        
    print ("Paso 5 completado con éxito")
    print()

    print ("Paso 6: Verificar que no existen tareas caducadas")
    response_fetched_complete_expired  = requests.get(url_test_fetch, timeout=request_timeout)
    url_test_complete_expired = get_base_url() + f"/tasks/caducadas"
    response_fetched_complete_expired  = requests.get(url_test_complete_expired, timeout=request_timeout)
    print (f"Respuesta previa al obtener tareas caducadas: {response_expired.json()}")
    print (f"Respuesta al obtener tareas caducadas: {response_fetched_complete_expired.json()}")
    assert response_fetched_complete_expired.status_code == 200, f"Codigo de respuesta incorrecto {response_fetched_complete_expired.status_code}. Se esperaba 200"
    assert response_fetched_complete_expired.json() == [], f"Detalle de error incorrecto ({response_fetched_complete_expired.json()})"
    print ("Paso 6 completado con éxito")
    print ()
    pass

def test_eliminar_tarea():

    print(f"Paso 1: Creacion de tarea")
    url_test_create = get_base_url() + "/tasks/"
    titulo= "Tarea de prueba - " + str(datetime.now())
    task_data={
        "titulo": titulo,
        "contenido": "Contenido de la tarea de prueba 'test_crear_tarea'",
        "deadline": (date.today() + timedelta(days=1)).isoformat()
    }

    response_created  = requests.post(url_test_create, json=task_data, timeout=request_timeout)
    print (f"Respuesta: {response_created.json()} Tarea_nueva: {task_data}")
    
    assert response_created.status_code == 201, f"Codigo de respuesta tarea creada incorrecto {response_created.status_code}. Se esperaba 201"
    assert response_created.json()["titulo"] == task_data["titulo"], f"El titulo de la tare creada no coincide ({task_data['titulo']} || {response_created.json()['titulo']})"
    assert response_created.json()["contenido"] == task_data["contenido"], f"El contenido de la tarea creada no coincide ({task_data['contenido']} || {response_created.json()['contenido']})"
    assert response_created.json()["deadline"] == task_data["deadline"], f"La fecha de vencimiento de la tarea creada no coincide ({str(task_data['deadline'])} || {response_created.json()['deadline']})"
    assert response_created.json()["completada"] == False, f"La tarea creada no debería estar completada al crearla ({response_created.json()['completada']})"
    assert "fecha_creacion" in response_created.json(), "La respuesta creada no contiene la fecha de creación"
    assert "id" in response_created.json(), "La respuesta creada no contiene el ID de la tarea"
    assert "fecha_modificacion" in response_created.json(), "La respuesta creada no contiene la fecha de modificación"

    print (f"Tarea creada exitosamente.")
    print ("Paso 1 completado con éxito")
    print ()

    print (f"Paso 2: Verificacion de obtener tarea contra tarea creada")
    task_id = response_created.json()["id"]    
    task_created=TaskResponse(**response_created.json())
    url_test_fetch = get_base_url() + f"/tasks/{task_id}"
    response_fetched  = requests.get(url_test_fetch, timeout=request_timeout)
    print (f"Respuesta: {response_fetched.json()} Tarea_nueva: {task_created}")
    assert response_fetched.status_code == 200, f"Codigo de respuesta tarea obtenida incorrecto {response_fetched.status_code}. Se esperaba 200"
    assert task_created.titulo == response_fetched.json()["titulo"], f"El titulo de la tarea obtenida no coincide con la tarea creada ({response_fetched.json()['titulo']} || {task_created.titulo})"
    assert task_created.contenido == response_fetched.json()["contenido"], f"El contenido de la tarea obtenida no coincide con la tarea creada ({response_fetched.json()['contenido']} || {task_created.contenido})"
    assert format_timestamp(str(task_created.deadline)) == format_timestamp(str(response_fetched.json()["deadline"])), f"La fecha de vencimiento de la tarea obtenida no coincide con la tarea creada ({format_timestamp(str(response_fetched.json()['deadline']))} || {format_timestamp(str(task_created.deadline))})"
    assert task_created.completada == response_fetched.json()["completada"], f"El estado de completado de la tarea obtenida no coincide con la tarea creada ({response_fetched.json()['completada']} || {task_created.completada})"
    assert format_timestamp(str(task_created.fecha_creacion)) == format_timestamp(str(response_fetched.json()["fecha_creacion"])), f"La fecha de creación de la tarea obtenida no coincide con la tarea creada ({format_timestamp(response_fetched.json()['fecha_creacion'])} || {format_timestamp(str(task_created.fecha_creacion))})"
    assert (format_timestamp(str(task_created.fecha_modificacion)) == format_timestamp(str(response_fetched.json()["fecha_modificacion"])) or (task_created.fecha_modificacion is None and response_fetched.json()["fecha_modificacion"] is None)), f"La fecha de modificación de la tarea obtenida no coincide con la tarea creada ({format_timestamp(str(response_fetched.json()['fecha_modificacion']))} || {format_timestamp(str(task_created.fecha_modificacion))})"
    print (f"Tarea obtenida exitosamente.")
    print ("Paso 2 completado con éxito")
    print ()

    print (f"Paso 3: Verificacion de obtener tarea contra datos iniciales")
    print (f"Respuesta: {response_fetched.json()} Tarea_nueva: {task_data}")
    assert response_fetched.json()["titulo"] == task_data["titulo"], f"El titulo de la tarea obtenida no coincide ({task_data['titulo']} || {response_fetched.json()['titulo']})"
    assert response_fetched.json()["contenido"] == task_data["contenido"], f"El contenido de la tarea obtenida no coincide ({task_data['contenido']} || {response_fetched.json()['contenido']})"
    assert response_fetched.json()["deadline"] == task_data["deadline"], f"La fecha de vencimiento de la tarea obtenida no coincide ({str(task_data['deadline'])} || {response_fetched.json()['deadline']})"
    assert response_fetched.json()["completada"] == False, f"La tarea obtenida no debería estar completada al crearla ({response_fetched.json()['completada']})"
    assert "fecha_creacion" in response_fetched.json(), "La respuesta obtenida no contiene la fecha de creación"
    assert "id" in response_fetched.json(), "La respuesta obtenida no contiene el ID de la tarea"
    assert "fecha_modificacion" in response_fetched.json(), "La respuesta obtenida no contiene la fecha de modificación"
    print (f"Tarea obtenida exitosamente.")
    print ("Paso 3 completado con éxito")
    print ()

    print ("Paso 4: Eliminar tarea")
    url_test_delete = get_base_url() + f"/tasks/{task_id}/eliminar"
    response_delete  = requests.delete(url_test_delete, timeout=request_timeout)  
    print (f"Respuesta: {response_delete.json() if response_delete.content else 'No Content'} Tarea_nueva: {url_test_delete}")
    assert response_delete.status_code == 204, f"Eliminando tarea, codigo de respuesta incorrecto {response_delete.status_code}. Se esperaba 204"
    assert response_delete.text == "", f"Eliminando tarea, la respuesta no debería contener contenido ({response_delete.text})"
    print ("Paso 4 completado con éxito")
    print ()

    print ("Paso 5: Recuperar tarea eliminada")
    response_fetched_delete  = requests.get(url_test_fetch, timeout=request_timeout)
    print (f"Respuesta: {response_fetched_delete.json()}")
    assert response_fetched_delete.status_code == 404, f"Codigo de respuesta tarea obtenida incorrecto {response_fetched_delete.status_code}. Se esperaba 404"
    assert response_fetched_delete.json()["detail"] == f"Tarea {task_id} no encontrada", f"Detalle de error incorrecto ({response_fetched_delete.json()['detail']})"
    assert "id" not in response_fetched_delete.json(), f"Detalle de error incorrecto ({response_fetched_delete.json()})"
    print (f"Tarea eliminada correctamente.")
    print ("Paso 5 completado con éxito")
    print ()
    pass



