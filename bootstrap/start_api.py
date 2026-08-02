import main
import uvicorn
import os

# Lee el puerto de la variable de entorno PORT, si no existe usa el 8000
port = int(os.getenv("API_PORT", 8080))
uvicorn.run("main:app", host="0.0.0.0", port=port)