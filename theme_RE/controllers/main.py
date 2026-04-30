from odoo import http
from odoo.http import request

class RealEstateController(http.Controller):
    @http.route('/propiedades', type='http', auth='public', website=True)
    def list_properties(self, **kwargs):
        print("\n\n >>> ¡EL CONTROLADOR ESTÁ FUNCIONANDO! <<< \n\n")
        # El .sudo() nos asegura que no haya errores de "Access Error"
        properties = request.env['real.estate'].sudo().search([])
        return request.render('theme_RE.properties_page', {
            'properties': properties,
        })
