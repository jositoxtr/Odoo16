from odoo import api, fields, models
from dateutil.relativedelta import relativedelta # Para calcular los 3 meses por defecto en date_avaliability
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

class Estate(models.Model):
    _name = 'real.estate'
    _description = 'Real Estate application'
    _order = "id desc"

    # Campos de datos
    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Avaliable from", default=lambda self: fields.Date.today() + relativedelta(months=3), copy=False)
    expected_price = fields.Float(string="Expected Price")
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (m2)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (m2)")
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north','North'),
                   ('south','South'),
                   ('east','East'),
                   ('west','West')],
        help="You can choose the orientation from your new home, here"
    )
    status = fields.Selection(
        string='Status',
        selection=[('new','New'),
                   ('offer_received','Offer received'),
                   ('offer_accepted','Offer accepted'),
                   ('sold','Sold'),
                   ('canceled', 'Canceled')],
                   default='new',
                   copy=False
    )
    active = fields.Boolean(string='Active', required=True, default=True)

    #Campos Relacionales
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    property_tag_ids = fields.Many2many("estate.property.tag", string="Property Tag")

    #Añadimos company_id (Requerido y con valor por defecto la compañía actual)
    company_id = fields.Many2one(
        'res.company', 
        string='Company', 
        required=True, 
        default=lambda self: self.env.company
    )

    salesperson_id = fields.Many2one(
        'res.users', 
        string='Salesperson', 
        #default=lambda self: self.env.user # Por defecto, el usuario que crea el registro
        default=False  # Se cambia de self.env.user a False por tu requisito
    )
    buyer_id = fields.Many2one(
        'res.partner', 
        string='Buyer', 
        copy=False # Para evitar que, al duplicar una propiedad, se duplique el comprador
    )
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    
    #Campos Computados
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area")
    best_offer = fields.Float(compute="_compute_best_offer", string="Best Offer")

    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    #Métodos
    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            record.best_offer = max(prices) if prices else 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        for record in self:
            if record.status == 'canceled':
                raise UserError("Properties that are canceled cannot be sold.")
            record.status = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.status == 'sold':
                raise UserError("Properties that are sold cannot be canceled.")
            record.status = 'canceled'
        return True
    
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_expected(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_rounding=0.01):
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_rounding=0.01) < 0:
                    raise ValidationError("The selling price can't be lower than 90 percent of the expected price")
    
    @api.ondelete(at_uninstall=False)
    def _check_state_before_deletion(self):
        for record in self:
            if record.status not in ('new', 'cancel'):
                raise UserError("You can't delete a property that is not 'New' or 'Canceled'.")

    