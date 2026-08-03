import os
import sys
from pathlib import Path

# Añade la carpeta 'python-api/src' al PYTHONPATH de forma dinámica
current_dir = Path(__file__).resolve().parent
src_path = current_dir.parent /  "unit_test"
sys.path.append(str(src_path))


from test_api import *

def main_test():

    print("Ejecutando tests...")
    print(get_base_url())
    print(get_database_url())

    # TODO: Llamar a las funciones de test y validar resultados

    print ()
    print ("Test: Creacion tarea")
    test_creacion_tarea()
    
    print ()
    print ("Test tareas caducadas")
    test_tareas_caducadas()

    print ()
    print ("Test: Eliminar tarea")
    test_eliminar_tarea()


