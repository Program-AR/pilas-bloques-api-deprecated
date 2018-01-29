import os
import sys

activate_this =  os.path.join(os.path.dirname(os.path.realpath(__file__)), 'venv/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

path = os.path.join(os.path.dirname(__file__))
if path not in sys.path:
        sys.path.append(path)

from app import app as application

