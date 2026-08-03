import subprocess
import os
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Configurar argparse para capturar el argumento --verbose
parser = argparse.ArgumentParser(description="Script para arrancar Docker Compose.")
parser.add_argument(
    "--verbose", 
    action="store_true", 
    help="Muestra la salida de Docker en tiempo real en la consola (capture_output=False)"
)
args = parser.parse_args()

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

# Si pasas --verbose, capture_output será False (verás los logs en directo)
# Si no lo pasas, será True (los oculta/captura en la variable)
activar_captura = not args.verbose

try:
    # Lanza el comando de docker compose usando el compose.yml
    resultado = subprocess.run(
        ["docker", "compose", "-f", str(compose_file_path), "up", "-d","--build"],
        check=True,
        text=True,
        capture_output=activar_captura
    )
    print("¡Contenedores arrancados con éxito!")
    print(resultado.stdout)
    
except subprocess.CalledProcessError as e:
    print("Error al ejecutar Docker Compose:")
    print(e.stderr)