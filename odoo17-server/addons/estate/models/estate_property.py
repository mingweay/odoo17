# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Description"

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Post Code')
    date_availability = fields.Datetime('Availability Date', copy=False,
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

