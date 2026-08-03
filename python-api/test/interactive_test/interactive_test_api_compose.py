import main_environment as test
import os

from dotenv import load_dotenv

# Carga las variables del archivo .env al entorno de ejecución
load_dotenv(override=True)
os.environ["API_PORT"] = "8100"
os.environ["DATABASE_USER"] = "postgres"
os.environ["DATABASE_PASSWORD"] = "secret123"
os.environ["DATABASE_SERVER"] = "localhost"
os.environ["DATABASE_PORT"] = "5432"
os.environ["DATABASE_CATALOG"] = "users"
print(f"Puerto de la API para pruebas: {test.get_port()}")
print(f"URL de la base de datos para pruebas: {test.get_database_url()}")
test.main_test()