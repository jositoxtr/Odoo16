from odoo import models, Command
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _inherit = "real.estate"

    def action_sold(self):
        for record in self:
            # 1. Verificar si el usuario tiene permiso de ESCRITURA en el modelo real.estate
            record.check_access_rights('write')
            
            # 2. Verificar si el usuario cumple las Record Rules para ESTA propiedad concreta
            record.check_access_rule('write')

        # Si las verificaciones fallan, Odoo lanzará un AccessError automáticamente aquí.
        # Si pasan, ejecutamos la lógica:
        
        res = super().action_sold()

        for record in self:
            self.env['account.move'].sudo().create({
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    (0, 0, {
                        'name': record.name,
                        'quantity': 1.0,
                        'price_unit': record.selling_price * 0.06,
                    }),
                    (0, 0, {
                        'name': 'Administrative fees',
                        'quantity': 1.0,
                        'price_unit': 100.0,
                    }),
                ],
            })
        return res

