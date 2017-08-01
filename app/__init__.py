from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS

from pylti.flask import lti

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Indique a continuacion el string de conexion a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////storage/db.sqlite'

# Esto para propagar excepciones - para debugging 
app.config.update(PROPAGATE_EXCEPTIONS = True)

db = SQLAlchemy(app)
CORS(app, supports_credentials=True)


#############################################################################
### logging para hacer un seguimiento del comportamiento del server y lti ###
#############################################################################

# import logging

# # create logger
# logger = logging.getLogger('pylti.flask')
# logger.setLevel(logging.DEBUG)

# logger2 = logging.getLogger('pylti.common')
# logger2.setLevel(logging.DEBUG)

# # create console handler and set level to debug
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)

# logger.addHandler(ch)
# logger2.addHandler(ch)

def set_debugging():
    """ enable debug logging
    """
    import logging
    import sys

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

set_debugging()

#############################################################################

import models
import schemas
import views


#############################################################################
######### configuracion para LTI: consumer_key -> shared_secret #############
#############################################################################

import os

# enable CSRF
app.config['WTF_CSRF_ENABLED'] = True

# secret key for authentication
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "you-will-never-guess")

# Sample client certificate example for 12 factor app
# You would want to store your entire pem in an environment variable
# with something like:
# ```
# export CONSUMER_KEY_CERT=$(cat <<EOF
# < paste cert here>
# EOF
# )
# ```

# app.config['CONSUMER_KEY_PEM_FILE'] = os.path.abspath('consumer_key.pem')
# with open(CONSUMER_KEY_PEM_FILE, 'w') as wfile:
# 	wfile.write(os.environ.get('CONSUMER_KEY_CERT', ''))

# Aqui completar key -> secret
# Lo ideal es que la pagina de PB permita configurar nuevos consumers directamente
app.config['PYLTI_CONFIG'] = {
    "consumers": {
        "__consumer_key__": {
            "secret": os.environ.get("CONSUMER_KEY_SECRET", "__lti_secret__"),
            #"cert": CONSUMER_KEY_PEM_FILE
        },
        "otrakey": {
        	"secret": "estesecret"
        }
    }
}

#############################################################################