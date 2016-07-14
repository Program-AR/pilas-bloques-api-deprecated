from marshmallow import Schema, fields

# SCHEMAS
# =======

class SolutionSchema(Schema):
    id = fields.UUID(dump_only=True)
    hash = fields.Str(required=True)
    usuario = fields.Str(required=True)
    desafio = fields.Str(required=True)
    xml = fields.Str(required=True)
    created_timestamp = fields.DateTime()


solutions_schema = SolutionSchema(many=True)
solution_schema = SolutionSchema()
