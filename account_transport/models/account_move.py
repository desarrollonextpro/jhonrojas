# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import xlrd
import tempfile
import binascii

from odoo import models, api, fields
from odoo.exceptions import UserError, ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    dispatch_sequence_id = fields.Many2one(
        comodel_name='ir.sequence',
        string=u'Guía de Remisión Electrónica',
        copy=False
    )
    picking_number = fields.Char(
        string=u'N° Guía',
        readonly=True,
        copy=False
    )
    prefix_val = fields.Char(
        string='Serie',
        copy=False
    )
    suffix_val = fields.Char(
        string='Correlativo',
        copy=False
    )
    dispatch_advice_state = fields.Selection([
        ('normal', 'Sin Enviar'),
        ('blocked', 'Rechazada'),
        ('done', 'Enviado')],
        string=u'Guía Electrónica',
        store=True
    )

    transfer_reason_id = fields.Many2one(
        comodel_name='transfer.reason.codes',
        string=u'Motivo de translado'
    )
    transfer_type_id = fields.Many2one(
        comodel_name='transfer.type.codes',
        string=u'Modalidad de translado'
    )
    scheduled_transfer = fields.Boolean(
        string=u'¿Transbordo programado?'
    )
    transfer_start_date = fields.Date(
        string=u'Fecha de Inicio del translado'
    )
    docker_number = fields.Char(
        string=u'N° de contendor'
    )
    code_port = fields.Char(
        string=u'Código del puerto'
    )
    transport_means = fields.Char(
        string=u'Número de Placa'
    )
    driver_id = fields.Many2one(
        comodel_name='res.partner',
        string=u'Conductor'
    )


class StockpikingDrivin(models.TransientModel):
    """
    excel import wizard in drivin.
    """
    _name = 'stock.piking.import.drivin'

    excel_file = fields.Binary('Cargar Driving')
    update_date = fields.Date('Fecha de Proceso')

    def action_stock_import_drivin(self):
        """ update file """
        lista_placa, lista_clientes = self.env['account.move.import.drivin'].read_excel(self.excel_file)
        active_ids = self._context.get('active_ids') or self._context.get('active_id')
        context = self.env['stock.picking'].browse(active_ids)
        drivers = self.env['res.partner'].search([])
        prefijo_drivin = self.env['ir.config_parameter'].get_param('prefijo_drivin')
        for record in context:
            for cliente, placa in zip(lista_clientes, lista_placa):
                cliente = cliente.strip(prefijo_drivin)
                cliente = int(cliente)
                if record.partner_id.id == cliente and record.scheduled_date == self.update_date:
                    if not record.transport_means:
                        record.write({'transport_means': placa})
                        for driver in drivers:
                            for line_driver in driver.vehicles:
                                if line_driver.license_plate == placa:
                                    record.write({'driver_id': driver})


class AccountMoveImportDrivin(models.TransientModel):
    """
    excel import wizard in drivin.
    """
    _name = 'account.move.import.drivin'

    excel_file = fields.Binary('Cargar Driving')
    update_date = fields.Date('Fecha de Proceso')

    def read_excel(self, file):
        """read excel"""
        try:
            fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
            fp.write(binascii.a2b_base64(file))
            fp.seek(0)
            workbook = xlrd.open_workbook(fp.name)
        except xlrd.biffh.XLRDError:
            raise UserError('Sólo se admiten archivos de Excel.')

        sheet = workbook.sheet_by_index(0)
        num_rows = sheet.nrows
        num_col = sheet.ncols
        lista_placa = []
        lista_clientes = []

        for cols in range(num_col):
            for rows in range(num_rows):
                cell = sheet.cell(rows, cols)
                if cols == 0:
                    if rows != 0:
                        lista_placa.append(cell.value)
                else:
                    if rows != 0:
                        lista_clientes.append(cell.value)
        return lista_placa, lista_clientes

    def action_account_import_drivin(self):
        """ update file """

        lista_placa, lista_clientes = self.read_excel(self.excel_file)
        active_ids = self._context.get('active_ids') or self._context.get('active_id')
        context = self.env['account.move'].browse(active_ids)
        drivers = self.env['res.partner'].search([])
        prefijo_drivin = self.env['ir.config_parameter'].get_param('prefijo_drivin')
        for record in context:
            for cliente, placa in zip(lista_clientes, lista_placa):
                cliente = cliente.strip(prefijo_drivin)
                cliente = int(cliente)
                if record.partner_id.id == cliente and record.invoice_date == self.update_date:
                    if not record.transport_means:
                        record.write({'transport_means': placa})
                        for driver in drivers:
                            for line_driver in driver.vehicles:
                                if line_driver.license_plate == placa:
                                    record.write({'driver_id': driver})
