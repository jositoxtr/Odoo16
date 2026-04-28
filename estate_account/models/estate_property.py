from odoo import models, Command
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _inherit = "real.estate"

    def action_sold(self):
        for record in self:
            if not record.buyer_id:
                raise UserError("No se puede vender una propiedad sin un comprador asignado.")
            
        # 1. Ejecutamos la lógica original del módulo estate
        res = super().action_sold()

        # 2. Creamos la factura para el comprador
        for record in self:
            self.env["account.move"].create({
                "partner_id": record.buyer_id.id, # Asegúrate que existe un comprador
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    # Línea de la comisión (6%)
                    Command.create({
                        "name": f"Comisión venta: {record.name}",
                        "quantity": 1.0,
                        "price_unit": record.selling_price * 0.06,
                    }),
                    # Línea de gastos fijos (100.00)
                    Command.create({
                        "name": "Gastos administrativos",
                        "quantity": 1.0,
                        "price_unit": 100.0,
                    }),
                ],
            })
        return res

