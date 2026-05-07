from odoo import fields, models

class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "real.estate", 
        "salesperson_id", 
        string="Properties",
        domain=[('status', 'in', ['new', 'offer_received'])] # Opcional: solo ver disponibles
    )