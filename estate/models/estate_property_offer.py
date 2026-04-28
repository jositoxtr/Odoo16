from odoo import api, fields, models
from datetime import timedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name='estate.property.offer'
    _order = "price desc"
    _description = 'Real Estate offers'

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('real.estate', required=True)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date (string="Deadline",  compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", string="Property Type", store=True)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            # Si el registro es nuevo, create_date es False, usamos la fecha de hoy
            date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Date.today()
            # Calculamos la diferencia de días para actualizar 'validity'
            record.validity = (record.date_deadline - date).days
    
    def action_accept(self):
        for record in self:
            # 1. Cambiar el estado de la oferta
            record.status = 'accepted'
            # 2. Asignar el comprador y el precio de venta a la propiedad
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            # 3. Cambiar el estado de la propiedad
            record.property_id.status = 'offer_accepted'
        return True

    def action_refuse(self):
        for record in self:
        # 1. Cambiar estado de la oferta
            record.status = 'refused'
        
        # 2. Si rechazamos la oferta aceptada, limpiamos la propiedad
        if record.property_id.buyer_id == record.partner_id:
            record.property_id.buyer_id = False
            record.property_id.selling_price = 0
            record.property_id.status = 'offer_received'
        return True
    
    @api.model
    def create(self, vals):
        # 1. Obtener la propiedad usando browse (porque property_id en vals es un ID entero)
        property_rec = self.env['real.estate'].browse(vals['property_id'])
        
        # 2. Validar que la oferta no sea menor a una existente
        if property_rec.offer_ids:
            max_offer = max(property_rec.offer_ids.mapped('price'))
            if vals['price'] < max_offer:
                raise UserError(f"The offer should be higher than the current one ({max_offer}).")
        
        # 3. Cambiar el estado de la propiedad a 'Offer Received'
        property_rec.status = 'offer_received'
        
        return super().create(vals)
