from odoo import _, api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'
    _description = 'Project Task'

    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    partner_id = fields.Many2one('res.partner', string='Partner')

    def onchange_to_last_stage(self):
        if self.env.ref('custom_project.custom_task_test').id == self.project_id.id and self.stage_id.id == self.env.ref('custom_project.stage_tree').id:
            self.sale_order_id.state = 'sale'
