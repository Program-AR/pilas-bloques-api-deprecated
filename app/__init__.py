from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Indique a continuacion el string de conexion a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////storage/db.sqlite'

db = SQLAlchemy(app)
CORS(app)

import models
import schemas
import views
