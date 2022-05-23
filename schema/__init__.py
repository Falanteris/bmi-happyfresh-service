from marshmallow import Schema, fields

class BMISchema(Schema):
    weight = fields.Integer(required=True,min=35)
    height = fields.Integer(required=True)
