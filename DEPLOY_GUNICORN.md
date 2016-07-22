Deploy de pilas-bloques-api en servidor de producción
=======================================================

Este guía indica como instalar la aplicación pilas-bloques-api en el entorno de producción sobre un servidor GNU/Linux. Se utiliza PostreSQL para almacenar datos y gunicorn+nginx para publicar la aplicación en un virtual host.

Instalación de la aplicación
---------------

Primero, se debe clonar el código de la aplicación desde este repositorio.

    git clone URL_REPO

Luego, es necesario crear un entorno virtual para python, con esto todas las dependencias y la aplicación quedarán aisladas del entorno.

    cd pilas-bloques-api
    pip install virtualenv
    virtualenv venv --no-site-packages
    . venv/bin/activate
    make init

Configuración del servidor de base de datos
---------------------

pilas-bloques-api puede ser utilizado con distintos motores de bases de datos, como MySQL, PostgreSQL o SQLite. En esta guía utilizamos PostgreSQL.

Una vez instalado el servidor, es necesario crear un usuario para la aplicación, llamaremos "pilas-bloques-api" a este usuario:

    createuser -D -e -P pilas-bloques-api

Al ejecutar el comando anterior el mismo solicitara la contraseña del usuario a crear.

Finalmente, se debe crear la base de datos:

    createdb -O pilas-bloques-api -E utf8 pilas-bloques-api


Configuración de la conexión a la base de datos
----------------------------------------------

Es necesario instalar psycopg2, un driver que permite utilizar bases de datos PostgreSQL desde python.

Se debe instalar en primer lugar la librería libpq5 y las cabeceras libpq-dev, en distribuciones de Linux derivadas de Debian esto puede hacer de la siguiente forma:

    apt-get install libpq5 libpq-dev

Luego, mediante pip instalar psycopg2:

    pip install psycopg2

A continuación, editar el archivo app/\__init.py__ para indicar los parámetros de la conexión a la base de datos, para esto modificar el valor del parámetro `app.config['SQLALCHEMY_DATABASE_URI']`:

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://pilas-bloques-api:pilas@localhost/pilas-bloques-api'

Asegurarse que el servidor admita conexiones TCP para el usuario pilas-bloques-api. Agregar al final del archivo `/etc/postgresql/9.4/main/pg_hba.conf` la siguiente línea:

    host    pilas-bloques-api             pilas-bloques-api             127.0.0.1/32            md5

Finalmente, inicializar la base de datos ejecutando:

    make initdb

Configuración de usuario de sistema para la aplicación
-----------------------------

Es aconsejable crear un usuario y un grupo específico para la ejecución de la aplicación.

    adduser --disabled-password --disabled-login pilas-bloques-api

Configuración de directorio de logs:
-------------------------

    mkdir PATH_AL_REPOSITORIO_CLONADO/logs
    chown pilas-bloques-api:pilas-bloques-api PATH_AL_REPOSITORIO_CLONADO/logs
    mkdir PATH_AL_REPOSITORIO_CLONADO/httpd-logs
    chown www-data:www-data PATH_AL_REPOSITORIO_CLONADO/httpd-logs


Configurar supervisord
-----------------------------

Para que inicie la aplicación. Debe crearse el archivo /etc/supervisor/conf.d/pilas-bloques-api.conf con el siguiente contenido, reemplazando PATH_AL_REPOSITORIO_CLONADO por el path corresponiente:

    [program:pilas-bloques-api]
    command=PATH_AL_REPOSITORIO_CLONADO/venv/bin/gunicorn run:app --workers=5 -b 0.0.0.0:8000
    directory=PATH_AL_REPOSITORIO_CLONADO
    user=pilas-bloques-api
    autostart=true
    autorestart=true
    redirect_stderr=true
    environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8
    stderr_logfile=PATH_AL_REPOSITORIO_CLONADO/logs/error.log
    stderr_logfile_maxbytes=1MB
    stderr_logfile_backups=10
    stderr_events_enabled=false

Detener e iniciar supervisor

    service supervisor stop
    service supervisor start

Configuración de nginx como proxy
--------------------

A continuación la aplicación puede publicarse en un virtual host `example.com` utilizando la siguiente configuración de nginx:

    server {
       listen   80; ## listen for ipv4; this line is default and implied

       server_name example.com;
       error_log PATH_AL_REPOSITORIO_CLONADO/httpd-logs/error.log error;

       location / {
           proxy_pass         http://127.0.0.1:8000/;
           proxy_redirect     off;

           proxy_set_header   Host                 $host;
           proxy_set_header   X-Real-IP            $remote_addr;
           proxy_set_header   X-Forwarded-For      $proxy_add_x_forwarded_for;
           proxy_set_header   X-Forwarded-Proto    $scheme;
       }
    }

Finalmente, reiniciar el servidor nginx.

Prueba
-----------------------

Pueden utilizarse los ejemplos de curl del archivo README.md para probar el funcionamiento de la aplicación.
