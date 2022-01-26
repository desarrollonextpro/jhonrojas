from odoo import fields, models, api
from odoo.exceptions import ValidationError


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
            raise ValidationError('El monto estimado no es mayor a 100.')
        elif self.order_type == 'especial' and self.estimated_amount <= 1000:
            raise ValidationError('El monto estimado no es mayor a 1000.')

        if len(self.order_line) > 3:
            raise ValidationError('La cantidad de líneas ingresas es mayor a 3.')

        for order_line in self.order_line:
            if order_line.product_uom_qty > 10:
                raise ValidationError('No puede comprar más de 10  artículos por línea en una misma orden de venta.')

        products = self.order_line.mapped('product_id.id')
        unique_products = set(products)

        if len(unique_products) != len(self.order_line):
            raise ValidationError('Hay artículos (productos) repetidos en otras líneas.')

        if self.anticipe_amount > self.estimated_amount:
            raise ValidationError('El monto anticipado es mayor al monto estimado.')

        if self.partner_shipping_id and self.partner_shipping_id.type != 'delivery':
            raise ValidationError('La dirección de envío no es de tipo envío')

        if self.partner_invoice_id and self.partner_invoice_id.type != 'invoice':
            raise ValidationError('La dirección de facturación no es de tipo factura')

    def assign_value(self):
        self.remainig_amount = self.estimated_amount - self.anticipe_amount
