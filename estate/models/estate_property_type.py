from odoo import fields, models

class EstatePropertyType(models.Model):
    _name='estate.property.type'
    _description='Property Type'
    _order = "sequence"

    sequence = fields.Integer('Sequence', default=1)   
    name=fields.Char(string="Name", required=True)
    property_ids = fields.One2many("real.estate", "property_type_id", string="Properties")
    offer_count = fields.Integer(compute="_compute_offer_count")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
