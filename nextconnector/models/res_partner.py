# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning
import requests
import json  
from . import popup_message
import logging
from . import util
_rq = util.util.request
_popup = popup_message.popup_message
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'
    over_credit = fields.Boolean('Permitir exceder limite de credito?')
    
    nxt_sync = fields.Selection(string="Estado de sincronización",selection=[("S","Sincronizado"),("N","No sincronizado"),("E","Error de sincronizacion")],default="N")
    nxt_id_erp = fields.Char('Código ERP')
    nxt_balance = fields.Float("Saldo de Cuenta")
    nxt_due_balance = fields.Float("Saldo Vencido")
    nxt_is_b2b = fields.Boolean("Es cliente B2B")

    def synchronize_customer(self):
        for record in self:
            #if record.nxt_sync == "E":
            #    return True

            data_obj = record.env["nextconnector.template_data"].search([('model','=',record._name)], limit=1)
            if data_obj.state != True: 
                return True

            results_vars = {}
            exec(data_obj.template_content, {"record":record,"env":self.env, "_logger":_logger},results_vars)

            response = _rq(self,"/nextconnector/api/records/customer",results_vars["json_data"],"post")

            if response["status_code"] != "200":
                self.write({"nxt_sync":'E'})
                self.message_post(body="Error de comunicación al sincronizar registro")
            else:
                json_resp = response["response_json"]
                if json_resp["code"] != "0":
                    self.write({"nxt_sync":'E'})
                    self.message_post(body=json_resp["message"])
                #else:   
                    #self.write({"nxt_sync":'S'})
                    #self.message_post(body="Registro sincronizado con ERP.")
    
    def post_customer(self, params):
        
        data_obj = self.env["nextconnector.template_query"].search([('code','=',"data_customer"),('state','=',True) ], limit=1)
        if not data_obj: 
            return True

        results_vars = {}
        exec(data_obj.template_content, {"env":self.env, "record": params , "_logger":_logger},results_vars)

        response = _rq(self,"/nextconnector/api/records/customer",results_vars["json_data"],"get")

        if response["status_code"] != "200":
            return _popup.error(self, "Error de comunicación")
        else:
            json_resp = response["response_json"]
            if json_resp["code"] != "0":
                return _popup.error(self, json_resp["message"])
            else:
                for list_data in json_resp["list_data"] :
                    for row in list_data["data"] :
                        try:
                            data_obj = self.env["nextconnector.template_query"].search([('code','=',"normalize_data_customer"),('state','=',True) ], limit=1)
                            if data_obj.state != True: 
                                    return True

                            results_vars = {}
                            exec(data_obj.template_content, {"env":self.env, "record": row , "_logger":_logger},results_vars)

                            _logger.error("INFO POST :" + str(results_vars["json_data"]))
                            
                        except Exception as e:
                            _logger.info("Error al crear cliente :" + str(e))
                            raise Warning("Error al crear cliente :" + str(e))
    
    def get_customer_balance(self):
        for record in self:
            data_obj = self.env["nextconnector.template_query"].search([('code','=',"data_customer_balance"),('state','=',True) ], limit=1)
            if not data_obj: 
                return True

            results_vars = {}
            exec(data_obj.template_content, {"env":self.env, "record": record, "_logger":_logger},results_vars)

            response = _rq(self,"/nextconnector/api/records/customer",results_vars["json_data"],"get")

            if response["status_code"] != "200":
                return _popup.error(self, "Error de comunicación")
            else:
                json_resp = response["response_json"]
                if json_resp["code"] != "0":
                    return _popup.error(self, json_resp["message"])
                else:
                    for list_data in json_resp["list_data"] :
                        for row in list_data["data"] :    
                            try:
                                data_obj = self.env["nextconnector.template_query"].search([('code','=',"normalize_data_customer_balance"),('state','=',True) ], limit=1)
                                if data_obj.state != True: 
                                        return True

                                results_vars = {}
                                exec(data_obj.template_content, {"env":self.env, "record": row , "_logger":_logger},results_vars)

                                _logger.error("INFO POST :" + str(results_vars["json_data"]))
                                #rec.action_done()
                                return _popup.success(self, "Importacion de datos de balance culminada.")
                            except Exception as e:
                                _logger.info("Error al consultar balance de cliente :" + str(e))
                                raise Warning("Error al consultar balance de cliente :" + str(e))

    
    
