import uuid
import datetime
import base64

from app import app, db
from sqlalchemy_utils import UUIDType

class Solution(db.Model):
    __tablename__ = "solution"

    id = db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    hash = db.Column(db.String(256), unique=True)
    usuario = db.Column(db.String(256), unique=False)
    desafio = db.Column(db.String(256), unique=False)
    xml = db.Column(db.Text(), unique=False)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, hash, usuario, desafio, xml):
        self.usuario = usuario
        self.desafio = desafio
        self.xml = xml
        self.hash = hash

    def __repr__(self):
        params = (self.hash, self.usuario, self.desafio)
        return '<Desafio: %s del usuario %s para el desafio %s>' % params
