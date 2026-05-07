from odoo.tests.common import TransactionCase
from odoo.tests import tagged

@tagged('post_install', '-at_install', 'estate')
class TestGardenReset(TransactionCase):

    def test_garden_reset_logic(self):
        """Verificar que al desmarcar 'garden', se limpian el área y la orientación"""
        # 1. Creamos propiedad con jardín
        prop = self.env['real.estate'].create({
            'name': 'Casa con Jardín',
            'garden': True,
            'garden_area': 50,
            'garden_orientation': 'south',
        })

        # 2. Simulamos que el usuario desmarca la casilla
        prop.garden = False
        
        # 3. Forzamos la ejecución del onchange (en los tests hay que llamarlo manualmente)
        prop._onchange_garden()

        # 4. Verificaciones
        self.assertEqual(prop.garden_area, 0, "El área del jardín no se reseteó a 0")
        self.assertFalse(prop.garden_orientation, "La orientación no se limpió")
