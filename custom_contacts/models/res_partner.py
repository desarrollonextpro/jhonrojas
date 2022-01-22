from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'Partner'

    category = fields.Char('Category')
    partner_id = fields.Many2one('res.partner', string='Partner')
    res_country_state_ids = fields.Many2many('res.country.state', string='States')
    partner_email = fields.Char(related='partner_id.email', string='Email of partner')
