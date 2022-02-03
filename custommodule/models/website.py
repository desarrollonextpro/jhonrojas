# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID
from odoo.exceptions import Warning
from odoo.http import request
from odoo.addons.website.models import ir_http
import json  
import logging
_logger = logging.getLogger(__name__)

class Website(models.Model):
    _inherit = 'website'

    default_pricelist_id = fields.Many2one('product.pricelist', string='Lista de precios por defecto')


    
   