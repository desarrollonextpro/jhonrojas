from odoo import fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"
    special_category = fields.Many2many('custommodule.special_category',string='Categorias especiales')
    is_quote = fields.Boolean('Articulo para cotización')

    url_afiliado = fields.Char(string='URL Afiliado')
    unidades_por_caja = fields.Float(string='Unidades por caja')
    proveedor_compra = fields.Many2one('res.partner',string='Proveedor asociado de compra')