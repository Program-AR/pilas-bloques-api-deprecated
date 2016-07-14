#!/usr/bin/python

import os
import sys

path = os.path.join(os.path.dirname(__file__))
activate_this = path + '/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

path = os.path.join(os.path.dirname(__file__))
if path not in sys.path:
    sys.path.append(path)

from flup.server.fcgi import WSGIServer
from app import app

if __name__ == '__main__':
    WSGIServer(app).run()

