from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged

@tagged('post_install', '-at_install', 'estate')
class TestEstateExercise(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.comprador = cls.env['res.partner'].create({'name': 'Test Buyer'})
        cls.propiedad = cls.env['real.estate'].create({
            'name': 'Propiedad Test',
            'expected_price': 100000,
            'status': 'new',
        })

    def test_01_no_offer_on_sold_property(self):
        """No se puede crear oferta si la propiedad está vendida"""
        self.propiedad.status = 'sold'
        with self.assertRaises(UserError, msg="Debería impedir crear oferta en propiedad vendida"):
            self.env['estate.property.offer'].create({
                'price': 90000,
                'partner_id': self.comprador.id,
                'property_id': self.propiedad.id,
            })

    def test_02_no_sell_without_accepted_offer(self):
        """No se puede vender si no hay ofertas aceptadas"""
        # Intentamos vender directamente (estando en 'new' o 'offer_received' pero sin aceptar ninguna)
        with self.assertRaises(UserError, msg="Debería impedir la venta sin oferta aceptada"):
            self.propiedad.action_sold()

    def test_03_successful_sell_workflow(self):
        """Venta correcta: crear oferta -> aceptar -> vender -> verificar estado"""
        # 1. Crear oferta
        oferta = self.env['estate.property.offer'].create({
            'price': 110000,
            'partner_id': self.comprador.id,
            'property_id': self.propiedad.id,
        })
        # 2. Aceptar oferta (esto ejecuta tu método action_accept)
        oferta.action_accept()
        self.assertEqual(self.propiedad.status, 'offer_accepted')

        # 3. Vender
        self.propiedad.action_sold()
        
        # 4. Verificación final: ¿Está vendida?
        self.assertEqual(self.propiedad.status, 'sold', "La propiedad debería estar marcada como 'sold'")
