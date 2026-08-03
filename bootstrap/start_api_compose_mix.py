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


current_dir = Path(__file__).resolve().parent
compose_python_file_path = current_dir.parent /  "compose_python.yml"
compose_postgres_file_path = current_dir.parent /  "compose_postgres.yml"

# Si pasas --verbose, capture_output será False (verás los logs en directo)
# Si no lo pasas, será True (los oculta/captura en la variable)
activar_captura = not args.verbose

try:
    # Lanza el comando de docker compose usando el compose.yml
    print(str(compose_postgres_file_path))
    resultado = subprocess.run(
        ["docker", "compose", "-f", str(compose_postgres_file_path),"-p","python-api", "up", "-d","--build"],
        check=True,
        text=True,
        capture_output=activar_captura
    )
    print(str(compose_python_file_path))
    resultado = subprocess.run(
        ["docker", "compose", "-f", str(compose_python_file_path),"-p","python-api", "up", "-d","--build"],
        check=True,
        text=True,
        capture_output=activar_captura
    )
    print("¡Contenedores arrancados con éxito!")

    
except subprocess.CalledProcessError as e:
    print("Error al ejecutar Docker Compose:")
    print(e.stderr)