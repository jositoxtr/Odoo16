from odoo import fields, models

class EstatePropertyType(models.Model):
    _name='estate.property.type'
    _description='Property Type'
    _order = "sequence"
 

    # Campos de datos 
    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer('Sequence', default=1) 

    #Campos Relacionales
    property_ids = fields.One2many("real.estate", "property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")

    # Campos computados
    offer_count = fields.Integer(compute="_compute_offer_count")

    #Métodos
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
