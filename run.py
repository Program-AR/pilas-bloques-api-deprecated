import os
from app import app

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
