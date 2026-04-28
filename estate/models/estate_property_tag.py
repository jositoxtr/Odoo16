from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name='estate.property.tag'
    _description='Property Tag'
    _order = "sequence, name desc"

    #Campos de datos
    sequence = fields.Integer("Sequence", default=1)
    name = fields.Char(string="Name", required=True)
    color = fields.Integer("Color")
    