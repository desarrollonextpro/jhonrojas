# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import requests
import json 
import logging
_logger = logging.getLogger(__name__)

class util(models.TransientModel):
    _name="nextconnector.util"
    _description = "Metodos utilitarios generales"

    def request(self, route, record, type):
        env_production = bool(self.env['ir.config_parameter'].sudo().get_param('nextconnector.env_production', default=False))
        url_api = str(self.env['ir.config_parameter'].sudo().get_param('nextconnector.url_api', default=""))
        user = str(self.env['ir.config_parameter'].sudo().get_param('nextconnector.user_api', default="nextpro"))
        password = str(self.env['ir.config_parameter'].sudo().get_param('nextconnector.pwd_api', default="N3xtPr0"))
        _logger.error("env_production :" + str(env_production))
        _logger.error("url_api :" + str(url_api))

        url = ""
        if env_production == True: 
            url = url_api + '/produccion'
        else:
            url = url_api + '/desarrollo'


        #SETEO DE URL DE SERVICIO REST
        url = url + route 

        bodyjson = {
            "credentials": {
                "user": user,
                "password": password
            },
            "record": record
        }

        responseObj = {"status_code":"404", "response_json":""}
        try:
            _logger.info("url :" + url + " requests :" +json.dumps(bodyjson))
            headers = {'content-type': 'application/json'}
            if type == "get":
                response = requests.get(url, data=json.dumps(bodyjson), headers=headers) #, timeout=(5, 100) )
            else:
                response = requests.post(url, data=json.dumps(bodyjson), headers=headers) #, timeout=(5, 100))
            
            _logger.info("response.status_code :" + str(response.status_code)+ " Json :" + json.dumps(response.json()) )
            responseObj["status_code"] = str(response.status_code)
            responseObj["response_json"] = response.json()
            return responseObj
            

        except requests.exceptions.ConnectionError as e:
            _logger.error("Error en consulta de web services!! :" + str(e))
            return responseObj

