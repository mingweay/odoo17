# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from dateutil.relativedelta import relativedelta



class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"

    price = fields.Float('price')
    status = fields.Selection(
        string='Offer Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Properties", required=True)

    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date('Deadline', compute="_compute_deadline", inverse="_inverse_deadline")

    _sql_constraints = [
        ('price', 'CHECK(price >= 0)',
         'The offer price should be strictly positive.'),
    ]


    @api.depends("validity", 'create_date')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def action_accept(self):
        for record in self:
            record.property_id.selling_price = self.price
            record.property_id.buyer = self.partner_id
            record.status = 'accepted'
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True


