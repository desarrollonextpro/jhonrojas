# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import random
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, models, fields, _
from odoo.http import request
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"
    payment_web_site = fields.Many2one('payment.acquirer',string='Metodo de pago web')
    state_shipping_erp = fields.Selection(string="Estado de despacho",selection=[("done","Entregado"),("pending","Pendiente"),("partial","Entrega parcial")],default="pending")

    tracking_number = fields.Char(string='Número de tracking')
    tracking_url = fields.Char(string='URL de Tracking')
    state_quote = fields.Selection(string="Estado de cotización",selection=[("01_pendiente_cliente","Pendiente de aprobación")
    ,("02_aprobada_cliente","Aprobada por cliente >> Anticipo pendiente"),("03_produccion_pendiente","Anticipo confirmado >> Aprobación de arte")
    ,("04_produccion_en_proceso","Arte aprobado >> Producción en proceso"),("05_produccion_terminada","Produccion terminada >> Pago pendiente")
    ,("06_entrega_aprobada","Pago final confirmado >> Aprobado para entrega")
    ],default="01_pendiente_cliente")
    is_quote = fields.Boolean(string='Es cotización?')

    """
    def _get_delivery_methods(self):
        address = self.partner_shipping_id
        self.ensure_one()
        order = self.sudo().browse(self.id)
        return self.env['delivery.carrier'].sudo().search([('website_published', '=', True)]).available_carriers(address, order)

    
    def _check_carrier_quotation(self, force_carrier_id=None):
        _logger.error("Entro SaleOrder _check_carrier_quotation: " +str(self) + " force_carrier_id:" + str(force_carrier_id))
        self.ensure_one()
        DeliveryCarrier = self.env['delivery.carrier']

        if self.only_services:
            self.write({'carrier_id': None})
            self._remove_delivery_line()
            return True
        else:
            # attempt to use partner's preferred carrier
            if not force_carrier_id and self.partner_shipping_id.property_delivery_carrier_id:
                force_carrier_id = self.partner_shipping_id.property_delivery_carrier_id.id

            carrier = force_carrier_id and DeliveryCarrier.browse(force_carrier_id) or self.carrier_id
            available_carriers = self._get_delivery_methods()
            if carrier:
                if carrier not in available_carriers:
                    carrier = DeliveryCarrier
                else:
                    # set the forced carrier at the beginning of the list to be verfied first below
                    available_carriers -= carrier
                    available_carriers = carrier + available_carriers
            if force_carrier_id or not carrier or carrier not in available_carriers:
                for delivery in available_carriers:
                    verified_carrier = delivery._match_address(self.partner_shipping_id, self)
                    if verified_carrier:
                        carrier = delivery
                        break
                self.write({'carrier_id': carrier.id})
            self._remove_delivery_line()
            if carrier:
                res = carrier.rate_shipment(self)
                if res.get('success'):
                    self.set_delivery_line(carrier, res['price'])
                    self.delivery_rating_success = True
                    self.delivery_message = res['warning_message']
                else:
                    self.set_delivery_line(carrier, 0.0)
                    self.delivery_rating_success = False
                    self.delivery_message = res['error_message']

        return bool(carrier)
    """


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    quote_size = fields.Char(string='Tamaño')
    quote_quantity = fields.Integer(string='Cantidad')
    quote_id_erp = fields.Char(string='Código ERP')
