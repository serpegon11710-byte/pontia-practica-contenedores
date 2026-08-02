# Variables de entorno

API_PORT --> Puerto en el que escucha el API
DATABASE_SERVER --> Nombre del servidor de la BBDD
DATABASE_PORT --> Puerto en el que escucha el servdor de la BBDD
DATABASE_CATALOG --> Nombre de la base de datos del servidor postgres
DATABASE_USER --> Usuario de la BBDD
DATABASE_PASSWORD --> Contraseña del usuario de BBDD

# Arranque

Para arrancar de forma limpia, lanzar el comando "docker compse -d" e instanciará el api dentro del docker para que escuhe en el puerto API_PORT definido en las variables de entorno. La configuracion de BBDD es transparente, dado que cre la BBDD dentro del Docker.

Adicionalmente hay tres metodos de arranque por entorno (pensados para testing), definidos en la carpeta bootstrap

**start-apy.py** : Aranca el api con las variables de entorno definidas. Instancia el api en local ty requiere que la BBDD sea accesible desde el propio ghost local
**start-api.local.py** : Aranca el api con las variables definidas en el propio script. 
Con el scrip original, se instancia en el puerto 8200 y requiere que el servidor BBD exista en localhost y escuhce en el puerto 8500
**start-api-compose.py" : Crea un docker compose con las variables definidas en el propio script. 
Con el scrip original, el api se instancia en el puerto 8100. El resto de configuracion es transparente ya que cre la BBDD dentro del docker.

