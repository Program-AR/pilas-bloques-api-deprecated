from pylti.flask import lti
from flask import render_template
from flask import jsonify
from flask import request
from flask import redirect
from sqlalchemy import desc
import datetime
import re

from app import app, db, models, schemas

def error(exception=None):
    """ render error page
    :param exception: optional exception
    :return: the error.html template rendered
    """
    print(exception)
    return render_template('error.html')

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
@lti(request='initial', error=error, app=app)
def lti_request(lti=lti):
    # El url para este redirect deberia poder armarse dinamicamente,
    # ya que el hash no es mas que string_a_base_64(idActividad + "-" + idAlumno + "-" + X)
    # con X un dato conocido solo por el consumer y distinto para cada par actividad-alumno
    # (dada la especificacion LTI, X podria ser el resource_link_id)
    # return redirect("http://pilasbloques.program.ar/online/#/desafios/cursoAlumno/QWxpZW5Ub2NhQm90b24tZG9uUGVwaXRvLUhBU0hERU1P")
    return redirect("http://localhost:4200/#/desafios/cursoAlumno/QWxpZW5Ub2NhQm90b24tZG9uUGVwaXRvLUhBU0hERU1P")


@app.route("/grade/", methods=["POST"])
@lti(request='session', error=error, app=app)
def lti_grade(lti=lti):
    # Esta nota se hardcodea por comodidad ahora, luego deberia poder ser evaluada 
    # en funcion del desempenio del alumno en el ejercicio correspondiente.
    # Una forma es tener guardadas las notas por alumno-ejercicio
    # en una base de datos y consultarlas en este handler.
    # En principio, debe ser un decimal entre 0 y 1 inclusive.
    # Puede representar lo que se necesite: cuan bien se hizo, cuan completo, etc.
    lti.post_grade(1)
    # Seria mas prolijo hacer un try-except para handlear en caso de que el post_grade falle.
    return jsonify({'success': True})
