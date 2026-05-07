from odoo import http
from odoo.http import request

class EstateController(http.Controller):

    # Esta ruta permite entrar a: ://tu-odoo.com
    @http.route('/propiedad/<int:prop_id>', auth='public', website=True)
    def ver_propiedad(self, prop_id, **kwargs):
        # 1. Buscamos la propiedad en la base de datos por su ID
        # Usamos .sudo() para que un visitante público pueda leerla aunque no tenga permisos
        propiedad = request.env['real.estate'].sudo().browse(prop_id)

        if not propiedad.exists():
            return "<h1>Lo sentimos, esa propiedad no existe.</h1>"

        # 2. Mostramos una respuesta sencilla (puedes usar una plantilla QWeb luego)
        html_content = f"""
            <html>
                <body style="font-family: sans-serif; padding: 50px;">
                    <h1>{propiedad.name}</h1>
                    <p><strong>Precio:</strong> {propiedad.expected_price} €</p>
                    <p><strong>Descripción:</strong> {propiedad.description or 'Sin descripción'}</p>
                    <hr/>
                    <p>Estado: {propiedad.status.upper()}</p>
                </body>
            </html>
        """
        return html_content
