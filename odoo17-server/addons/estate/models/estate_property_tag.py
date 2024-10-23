# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from dateutil.relativedelta import relativedelta

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"

    name = fields.Char('Name', required=True)

    _sql_constraints = [
        ('check_tag', 'UNIQUE(name)',
         'The tag should be unique.')
    ]
