from odoo import _, api, fields, models

import logging


_logger = logging.getLogger(__name__)


class LoanLine(models.Model):
    _name = 'loan.line'
    _description = 'loan line'

    name = fields.Char('Name')
    payment_date = fields.Date('Payment Date')
    amount = fields.Float('Amount')
    loan_id = fields.Many2one('loan', string='Loan')
