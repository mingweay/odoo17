# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Description"

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Post Code')
    date_availability = fields.Date('Availability Date', copy=False,
                                        default=fields.Date.today() + relativedelta(months=+3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string="State",
        selection=[('new', 'New'), ('offer_received', 'Offer Received'),
                   ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancel', 'Cancelled')],
        copy=False,
        default='new',
        required=True,
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer = fields.Many2one("res.partner", string="Buyer")

    property_tag_ids = fields.Many2many("estate.property.tag", string="Property Tag")
    offer_ids = fields.One2many("estate.property.offer", 'property_id', string="Property Offers")

    total_area = fields.Integer('Total Area', compute="_compute_total_area")
    best_price = fields.Float('Best Offer', compute="_compute_best_price")

    _sql_constraints = [
        ('expected_price', 'CHECK(expected_price >= 0)',
         'The expected price should be strictly positive.'),
        ('selling_price', 'CHECK(selling_price >= 0)',
         'The selling price should be strictly positive.')
    ]

    @api.constrains('expected_price', 'selling_price')
    def check_price(self):
        for record in self:
            threshold = record.expected_price * 0.9
            if record.selling_price < threshold:
                raise ValidationError("Selling price cannot be lower than 90% of the expected price")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = self.garden_area + self.living_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10
        self.garden_orientation = "north"

    def action_sold(self):
        for record in self:
            if record.state != 'cancel':
                record.state = "sold"
            else:
                raise UserError("Cancelled properties cannot be sold.")
        return True

    def action_cancel(self):
        for record in self:
            record.state = "cancel"
        return True
