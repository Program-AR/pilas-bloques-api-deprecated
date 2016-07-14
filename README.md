pilas-bloques-api
=================

Un servidor que permite guardar y recuperar soluciones para la aplicación
pilas-bloques.

Este servidor se usa de forma conjunta a moodle y pilas-bloques.


¿Cómo instalar?
---------------

Primero, se tiene que crear un entorno virtual para python, con esto
todas las dependencias y la aplicación quedarán aisladas del entorno.

    pip install virtualenv
    virtualenv venv --no-site-packages
    . venv/bin/activate
    make init initdb

Notá que en los pasos anteriores también inicializamos la base de datos.

Luego vas a tener acceso a todos los comandos del sistema invocando a make:

    make


Por ejemplo, para correr los tests y luego iniciar la aplicación podemos
escribir:

    make test
    make run


Ejemplos de invocación desde consola
------------------------------------

Un ejemplo de invocación para crear un registro:

    ➤ curl -XPOST -H "Content-type: application/json" -d '{"usuario": "demo", "desafio": "alien", "hash": "123ddj", "xml": "<demo></demo>"}' 'http://localhost:5000/soluciones/'

        {"data": {
            "created_timestamp": "2016-07-09T04:51:56.842964+00:00", 
            "desafio": "alien", 
            "hash": "123ddj", 
            "id": "aec6370c-687d-46ad-8ad3-5c537b654516", 
            "usuario": "demo", 
            "xml": "<demo></demo>"
        }}


Como conseguir el mismo registro usando el parámetro hash:

    ➤ curl http://localhost:5000/soluciones/123ddj
