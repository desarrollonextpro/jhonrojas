from odoo import api, fields, models


class StockPiking(models.Model):
    _inherit = "stock.picking"
    
    scheduled_date = fields.Date(
        'Scheduled Date', compute='_compute_scheduled_date', inverse='_set_scheduled_date', store=True,
        index=True, default=fields.Datetime.now, tracking=True,
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        help="Scheduled time for the first part of the shipment to be processed. \
        Setting manually a value here would set it as expected date for all the stock moves.")