from odoo import fields, models


class SpecialCategory(models.Model):

    _name = 'custommodule.special_category'
    _description = 'Categoria especial'

    name = fields.Char('Categoria')
    description = fields.Char('Descripcion')