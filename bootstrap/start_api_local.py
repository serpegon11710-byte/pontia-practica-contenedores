import uvicorn
import os
from dotenv import load_dotenv
from pathlib import Path
import sys

# Añade la carpeta 'python-api/src' al PYTHONPATH de forma dinámica
current_dir = Path(__file__).resolve().parent
src_path = current_dir.parent /  "python-api/src"
sys.path.append(str(src_path))

from main import app

# Lee el puerto de la variable de entorno PORT, si no existe usa el 8000
load_dotenv(override=True)
os.environ["API_PORT"] = "8200"
os.environ["DATABASE_USER"] = "fastapi_user"
os.environ["DATABASE_PASSWORD"] = "secret123"
os.environ["DATABASE_SERVER"] = "localhost"
os.environ["DATABASE_PORT"] = "8500"
os.environ["DATABASE_CATALOG"] = "users"

print(f"Puerto de la API: {os.getenv('API_PORT', 8080)}")
print(f"URL de la base de datos: postgresql+psycopg2://{os.getenv('DATABASE_USER', 'none')}:{os.getenv('DATABASE_PASSWORD', 'none')}@{os.getenv('DATABASE_SERVER', 'none')}:{os.getenv('DATABASE_PORT', 'none')}/{os.getenv('DATABASE_CATALOG', 'none')}")
uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv('API_PORT', 8080)))