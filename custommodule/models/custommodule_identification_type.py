# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class IdentificationType(models.Model):

    _name = 'custommodule.identification.type'
    _description = 'Tipo de identificación'
    name = fields.Char(translate=True, required=True,)
    description = fields.Char()
    active = fields.Boolean(default=True)