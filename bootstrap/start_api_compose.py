import subprocess
import os
from pathlib import Path
from dotenv import load_dotenv

# Lee el puerto de la variable de entorno PORT, si no existe usa el 8000
load_dotenv(override=True)
os.environ["API_PORT"] = "8100"
os.environ["DATABASE_USER"] = "postgres"
os.environ["DATABASE_PASSWORD"] = "secret123"
os.environ["DATABASE_SERVER"] = "localhost"
os.environ["DATABASE_PORT"] = "5432"
os.environ["DATABASE_CATALOG"] = "users"

current_dir = Path(__file__).resolve().parent
compose_file_path = current_dir.parent /  "compose.yml"
print(str(compose_file_path))

try:
    # Lanza el comando de docker compose usando el compose.yml
    resultado = subprocess.run(
        ["docker", "compose", "-f", str(compose_file_path), "up", "-d"],
        check=True,
        text=True,
        capture_output=True
    )
    print("¡Contenedores arrancados con éxito!")
    print(resultado.stdout)
    
except subprocess.CalledProcessError as e:
    print("Error al ejecutar Docker Compose:")
    print(e.stderr)