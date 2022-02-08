from odoo import _, api, fields, models
from dateutil.relativedelta import relativedelta
import logging


_logger = logging.getLogger(__name__)


class Loan(models.Model):
    _name = 'loan'
    _description = 'Loan'

    name = fields.Char('Name')
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    date = fields.Date('Date')
    fees = fields.Integer('Fees')
    amount_total = fields.Float('Amount Total')
    line_ids = fields.One2many('loan.line', 'loan_id', string='Lines of loan')

    def generate_lines(self):
        if self.partner_id and self.date and self.fees and self.amount_total:
            amount = self.amount_total / self.fees
            records = []
            for line in range(self.fees):
                months = line+1
                dict = {}
                dict['amount'] = amount
                dict['payment_date'] = self.date_order + relativedelta(months=months)
                records.append((0, 0, dict))

            self.line_ids = records
