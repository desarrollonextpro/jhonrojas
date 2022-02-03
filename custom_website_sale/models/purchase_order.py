from odoo import _, api, fields, models

import logging


_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    _description = 'Purchase Order'

    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    website_id = fields.Many2one('website', string='Website')
