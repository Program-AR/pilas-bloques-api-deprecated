from flask import jsonify
from flask import request
from sqlalchemy import desc
import datetime
import re

from app import app, db, models, schemas

@app.route('/')
def index():
    return jsonify({'data': {'name': "pilas-bloques-api"}})

@app.route('/soluciones/<hash>')
def get_solutions_by_hash(hash):
    q = models.Solution.query.filter_by(hash=hash,)

    records = q.all()

    if not records:
        return jsonify({"error": "invalid hash"}), 400

    result = schemas.solutions_schema.dump(records)

    return jsonify({'data': result.data})

@app.route("/soluciones/", methods=["POST"])
def create_a_solution():
    json_data = request.get_json()

    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    data, errors = schemas.solution_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    last = models.Solution.query.filter_by(hash=data['hash']).one_or_none()

    if last:
        solution = last
        solution.xml = data['xml']
        solution.usuario = data['usuario']
        solution.desafio = data['desafio']
    else:
        solution = models.Solution(data['hash'], data['usuario'], data['desafio'], data['xml'])

    db.session.add(solution)
    db.session.commit()

    result = schemas.solution_schema.dump(solution)
    return jsonify({'data': result.data})

@app.route("/lti/")
def lti_welcome():
    return jsonify({'data': {'name': "pilas-bloques-lti-api"}})

@app.route("/lti/", methods=["POST"])
def lti_request():
    #request_data = request.get_json()
    request_data = request.form
    ok = True

    # Check it is a POST request
    ok = ok and (request.method == 'POST') # no aporta nada por ahora dado que esta funcion solo recibe post

    # Check the LTI message type
    ok = ok and request_data['lti_message_type'] and (request_data['lti_message_type'] == 'basic-lti-launch-request')

    # Check the LTI version
    ok = ok and request_data['lti_version'] and (request_data['lti_version'] == 'LTI-1p0')

    # Check a consumer key exists
    ok = ok and request_data['oauth_consumer_key']

    # Check a resource link ID exists
    ok = ok and request_data['resource_link_id']

    #if not request_data or not request_data['lti_version']:
    if not ok :
        return jsonify({'message': 'Not a valid LTI request'}), 400

    return jsonify({'message': 'your LTI request is for version: ' + request_data['lti_version'] })
