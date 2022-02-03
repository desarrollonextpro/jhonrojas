# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import Warning
import requests
import json  
import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'
    special_category = fields.Many2many('custommodule.special_category',string='Categorias especiales')
    first_name = fields.Char(string='Nombres')
    last_name = fields.Char(string='Apellidos')
    identification_type_id = fields.Many2one('custommodule.identification.type',
        string="Tipo de identificación")

    pedidos_pendientes = fields.Float("Pedidos pendientes")

    def customer_balance(self):
        
        for customer in self:
            if customer.nxt_id_erp and customer.nxt_is_b2b:
                customer.get_customer_balance()

            return customer
    
        
    
    
