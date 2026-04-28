from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name='estate.property.tag'
    _description='Property Tag'
    _order = "sequence, name desc"

    name=fields.Char(string="Name", required=True)
    color = fields.Integer("Color")
    sequence = fields.Integer("Sequence", default=1)