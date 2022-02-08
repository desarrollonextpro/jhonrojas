from odoo import _, api, fields, models
from dateutil.relativedelta import relativedelta
import logging
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


class Loan(models.Model):
    _name = 'loan'
    _description = 'Loan'

    name = fields.Char('Name')
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    date = fields.Date('Date', default=fields.Date.today())
    fees = fields.Integer('Fees')
    amount_total = fields.Float('Amount Total')
    line_ids = fields.One2many('loan.line', 'loan_id', string='Lines of loan')

    def generate_lines(self):
        if self.partner_id and self.date and self.fees and self.amount_total:
            self.line_ids = [(5, 0, 0)]
            amount = self.amount_total / self.fees
            records = []
            for line in range(self.fees):
                months = line+1
                dict = {}
                dict['amount'] = amount
                dict['payment_date'] = self.date + relativedelta(months=months)
                records.append((0, 0, dict))

            self.line_ids = records
        else:
            raise UserError('Ingrese socio, fecha, número de cuotas y monto total.')

    @api.model
    def create(self, vals):
        vals['name'] = f"Prestamo de {self.env['res.partner'].browse(vals.get('partner_id')).name or ''} en la fecha  {self.date.strftime('%d/%m/%Y')}"
        return super(Loan, self).create(vals)
