from odoo import models, fields


class TransferType(models.Model):
    _name = 'transfer.type'
    _description = 'Transfer Type'

    name = fields.Char('Name')
    code = fields.Char('Code')
