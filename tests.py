# coding: utf-8
import unittest
import base64
import json

from flask.ext.testing import TestCase

from app import app, db, models

class SpectroAPITests(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_main_route_must_return_200(self):
        response = self.client.get("/")
        self.assertEquals(200, response.status_code)

    def test_puede_consultar_por_hash_inexistente(self):
        response = self.client.get("/soluciones/HASH")
        self.assertEquals(400, response.status_code, "Se asegura que un registro inexistente retorna 400")

    def test_puede_guardar_una_solucion_desde_la_base_de_datos(self):
        usuario = "alumno1"
        desafio = "desafio1"
        xml = "<demo></demo>"
        salt_demo = "xxxxx" # debe ser generado del lado de moodle.
        hash = base64.b64encode(usuario + "-" + desafio + salt_demo)

        # Genera la solucion desde la base de datos.
        solution = models.Solution(hash, usuario, desafio, xml)
        db.session.add(solution)
        db.session.commit()

        assert solution in db.session

        # Consulta desde la api si ese registro se guardó o no.
        response = self.client.get("/soluciones/" + hash)
        self.assertEquals(len(response.json['data']), 1, "Se corrobora que hay un registro")

        registro = response.json['data'][0]

        self.assertEquals(registro['usuario'], usuario, "El nombre de alumno se recupera correctamente.")
        self.assertEquals(registro['desafio'], desafio, "El nombre del desafio se puede recuperar.")
        self.assertEquals(registro['xml'], xml, "La solución xml se recupera correctamente.")
        self.assertEquals(registro['hash'], hash, "El hash se recupera correctamente.")


    def test_puede_guardar_una_solucion_pero_desde_un_request(self):
        usuario = "alumno1"
        desafio = "desafio1"
        xml = "<demo></demo>"
        salt_demo = "xxxxx" # debe ser generado del lado de moodle.
        hash = base64.b64encode(usuario + "-" + desafio + salt_demo)

        data_json = {
            "usuario": usuario,
            "desafio": desafio,
            "xml": xml,
            "hash": hash
        }

        data = json.dumps(data_json)
        response = self.client.post("/soluciones/", data=data, content_type='application/json')

        response = self.client.get("/soluciones/" + hash)
        self.assertEquals(len(response.json['data']), 1, "Se corrobora que hay un registro")

        # TODO: corroborar que los datos se recuperan.

    def test_pretty_print_esta_deshabilitado(self):
        # TODO: verificar que la salida no tenga tabs
        #self.client.post("/2A/commands", data='{"command":"ls", "device": "2A"}', content_type='application/json')

        #response = self.client.get("/2A/commands?executed=false")
        #self.assertFalse('\\t' in response.data)
        pass


if __name__ == '__main__':
    unittest.main()
