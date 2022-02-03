from odoo import _, api, fields, models

import logging


_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale order'

    sales_order_generated = fields.Boolean('Sales order generated', default=False)

    def write(self, vals):

        _logger.info(f"""
                     
                         {self.sales_order_generated}
                    
                       """)

        if self.state == 'sale' and self.website_id and not self.sales_order_generated:
            supplier_ids = self.order_line.mapped('product_id.product_tmpl_id.proveedor_compra')

            try:
                _logger.info(supplier_ids)
            except:
                pass
            else:
                if supplier_ids:
                    for sp in supplier_ids:
                        order_lines = self.order_line.filtered(lambda olp:  olp.product_id.product_tmpl_id.proveedor_compra == sp)

                        new_order = self.env['purchase.order'].create({
                            'partner_id': sp.id,
                            'currency_id': self.currency_id.id,
                            'company_id': self.company_id.id,
                            'date_order': fields.Datetime.now(),
                            'sale_order_id': self.id,
                            'website_id': self.website_id.id
                        })

                        records = []

                        _logger.info("""
                                     
                                     self.state: {self.state}
                                     
                                     """)

                        for ol in order_lines:
                            dict = {}

                            dict['product_qty'] = ol.product_uom_qty

                            dict['name'] = ol.product_id.name
                            dict['product_id'] = ol.product_id.id
                            dict['product_uom'] = ol.product_uom.id
                            dict['price_unit'] = ol.price_unit
                            dict['date_planned'] = fields.Datetime.now()

                            records.append((0, 0, dict))

                        new_order.order_line = records

                    vals.update({'sales_order_generated': True})

        return super(SaleOrder, self).write(vals)
