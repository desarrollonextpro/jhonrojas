from odoo import fields, models, api
import logging


_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale Order'

    project_task_id = fields.Many2one('project.task', string='Project Task')

    def action_create_project_task(self):
        record = {
            'name': self.name + self.partner_id.name,
            'partner_id': self.partner_id.id,
            'sale_order_id': self.id,
            'project_id': self.env.ref('custom_project.custom_task_test').id,
            'stage_id': self.env.ref('custom_project.stage_one').id,
        }

        # TODO: por verificar si funciona ref como imagino

        _logger.info(f"""
                     
                     
                     RECORD: {record}
                     ID: {self.env.ref('custom_project.stage_one').id}                     
                     MORE INFO: {self.env.ref('custom_project.stage_one')}                     
                     
                     """)

        project_task = self.env['project.task'].sudo().create(record)

        self.project_task_id = project_task.id
