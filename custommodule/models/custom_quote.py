from odoo import fields, models


class  QuoteSize(models.Model):

    _name = 'custommodule.quote.size'
    _description = 'Presentaciones de cotización'

    name = fields.Char('Presentación')
    description = fields.Char('Descripcion')

class  QuoteQuantity(models.Model):

    _name = 'custommodule.quote.quantity'
    _description = 'Cantidades de cotización'

    name = fields.Integer('Cantidad')

class  QuoteProducts(models.Model):

    _name = 'custommodule.quote.products'
    _description = 'Productos de cotización'

    product_tmpl_id = fields.Many2one('product.template', 'Producto')
    quote_size = fields.Many2one('custommodule.quote.size',string="Presentacion")
    quote_quantity = fields.Many2one('custommodule.quote.quantity',string="Cantidad")
    quote_unit_case = fields.Integer('Unidades por caja')
    quote_price = fields.Float('Precio unitario', required=True, digits='Product Price', default=0.0)
    id_erp = fields.Char('Código ERP')
    
    

class ProductTemplate(models.Model):
    _inherit = "product.template"
    quote_product_ids = fields.One2many("custommodule.quote.products","product_tmpl_id")