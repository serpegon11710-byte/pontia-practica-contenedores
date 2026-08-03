import main_environment as test
import os
from dotenv import load_dotenv

# Carga las variables del archivo .env al entorno de ejecución
load_dotenv(override=True)
print(f"Puerto de la API para pruebas: {test.get_port()}")
print(f"URL de la base de datos para pruebas: {test.get_database_url()}")
test.main_test()
