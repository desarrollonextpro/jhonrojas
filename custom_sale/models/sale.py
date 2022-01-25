from odoo import fields, models, api
from odoo.exceptions import ValidationError
import logging


_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale Order'

    order_type = fields.Selection([
        ('normal', 'normal'),
        ('especial', 'especial')
    ], string='Order Type')

    estimated_amount = fields.Float('Estimated amount')
    transfer_type_id = fields.Many2one('transfer.type', string='Tranfer Type')
    anticipe_amount = fields.Float('Anticipe Amount')
    remainig_amount = fields.Float('Remainig Amount')

    # @api.depends('estimated_amount', 'anticipe_amount')
    # def compute_remaining_amount(self):
    #     self.remainig_amount = self.estimated_amount - self.anticipe_amount

    # @api.constrains('order_type')
    # def _constrains_order_type(self):
    #     if not (self.order_type == 'normal' and self.estimated_amount > 100):
    #         raise ValidationError('Error.')
    #     elif not (self.order_type == 'especial' and self.estimated_amount > 1000):
    #         raise ValidationError('Error.')

    # @api.constrains('order_line.product_uom_qty', 'order_line.product_id', 'order_line')
    # def _constrains_order_line(self):
    #     if len(self.order_line) > 3:
    #         raise ValidationError('Error.')

    #     for order_line in self.order_line:
    #         if order_line.product_uom_qty > 10:
    #             raise ValidationError('Error.')
    #     products = self.order_line.mapped('product_id')
    #     unique_products = set(products)

    #     if len(unique_products) != len(products):
    #         raise ValidationError('Error.')

    # @api.constrains('anticipe_amount', 'estimated_amount')
    # def _constrains_anticipe_estimated_amount(self):
    #     if self.anticipe_amount > self.estimated_amount:
    #         raise ValidationError('Error.')

    def validation_custom_sale(self):
        if self.order_type == 'normal' and self.estimated_amount <= 100:
            raise ValidationError('Error. 0')
        elif self.order_type == 'especial' and self.estimated_amount <= 1000:
            raise ValidationError('Error. 1')

        if len(self.order_line) > 3:
            raise ValidationError('Error. 2')

        for order_line in self.order_line:
            if order_line.product_uom_qty > 10:
                raise ValidationError('Error. 3')

        products = self.order_line.mapped('product_id.id')
        unique_products = set(products)

        _logger.info("\n\n\nMOSTRAR DATOS %s\n\n\n", [unique_products, products])
        _logger.info("\n\n\nMOSTRAR DATOS %s\n\n\n", [len(unique_products), len(self.order_line)])

        if len(unique_products) != len(self.order_line):
            raise ValidationError('Error. 4')

        if self.anticipe_amount > self.estimated_amount:
            raise ValidationError('Error. 5')

        if self.partner_shipping_id and self.partner_shipping_id.type != 'delivery':
            raise ValidationError('Error. 6')

        if self.partner_invoice_id and self.partner_invoice_id.type != 'invoice':
            raise ValidationError('Error. 7')

    def assign_value(self):
        self.remainig_amount = self.estimated_amount - self.anticipe_amount
