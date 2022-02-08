from odoo import fields, models, api
from odoo.exceptions import ValidationError
import paramiko
import logging
import pysftp
# import fnmatch


_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale Order'

    order_type = fields.Selection([
        ('normal', 'normal'),
        ('especial', 'especial')
    ], string='Order Type')

    estimated_amount = fields.Float('Estimated amount')
    transfer_type_id = fields.Many2one('transfer.type', string='Tranfer Type')
    anticipe_amount = fields.Float('Anticipe Amount')
    remainig_amount = fields.Float('Remainig Amount')

    # @api.depends('estimated_amount', 'anticipe_amount')
    # def compute_remaining_amount(self):
    #     self.remainig_amount = self.estimated_amount - self.anticipe_amount

    # @api.constrains('order_type')
    # def _constrains_order_type(self):
    #     if not (self.order_type == 'normal' and self.estimated_amount > 100):
    #         raise ValidationError('Error.')
    #     elif not (self.order_type == 'especial' and self.estimated_amount > 1000):
    #         raise ValidationError('Error.')

    # @api.constrains('order_line.product_uom_qty', 'order_line.product_id', 'order_line')
    # def _constrains_order_line(self):
    #     if len(self.order_line) > 3:
    #         raise ValidationError('Error.')

    #     for order_line in self.order_line:
    #         if order_line.product_uom_qty > 10:
    #             raise ValidationError('Error.')
    #     products = self.order_line.mapped('product_id')
    #     unique_products = set(products)

    #     if len(unique_products) != len(products):
    #         raise ValidationError('Error.')

    # @api.constrains('anticipe_amount', 'estimated_amount')
    # def _constrains_anticipe_estimated_amount(self):
    #     if self.anticipe_amount > self.estimated_amount:
    #         raise ValidationError('Error.')

    def validation_custom_sale(self):
        if self.order_type == 'normal' and self.estimated_amount <= 100:
            raise ValidationError('El monto estimado no es mayor a 100.')
        elif self.order_type == 'especial' and self.estimated_amount <= 1000:
            raise ValidationError('El monto estimado no es mayor a 1000.')

        if len(self.order_line) > 3:
            raise ValidationError('La cantidad de líneas ingresas es mayor a 3.')

        for order_line in self.order_line:
            if order_line.product_uom_qty > 10:
                raise ValidationError('No puede comprar más de 10  artículos por línea en una misma orden de venta.')

        products = self.order_line.mapped('product_id.id')
        unique_products = set(products)

        if len(unique_products) != len(self.order_line):
            raise ValidationError('Hay artículos (productos) repetidos en otras líneas.')

        if self.anticipe_amount > self.estimated_amount:
            raise ValidationError('El monto anticipado es mayor al monto estimado.')

        if self.partner_shipping_id and self.partner_shipping_id.type != 'delivery':
            raise ValidationError('La dirección de envío no es de tipo envío')

        if self.partner_invoice_id and self.partner_invoice_id.type != 'invoice':
            raise ValidationError('La dirección de facturación no es de tipo factura')

    def assign_value(self):
        self.remainig_amount = self.estimated_amount - self.anticipe_amount

    @api.model
    def create(self, vals):

        ftp_server = str(self.env['ir.config_parameter'].sudo().get_param('casa6_upload_ftp.ftp_server', default="173.201.184.177"))

        ftp_user = str(self.env['ir.config_parameter'].sudo().get_param('casa6_upload_ftp.ftp_user', default="test1@casa6m.com"))

        ftp_pwd = str(self.env['ir.config_parameter'].sudo().get_param('casa6_upload_ftp.ftp_pwd',
                                                                       default="/home/c5dcblxr83om/public_html/casa6m.com/test1"))

        ftp_path_out = str(self.env['ir.config_parameter'].sudo().get_param('casa6_upload_ftp.ftp_path_out', default="Figu123.."))

        # # Inicia un cliente SSH

        # ssh_client = paramiko.SSHClient()

        # # Establecer política por defecto para localizar la llave del host localmente

        # ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # # Conectarse
        # try:
        #     ssh_client.connect(ftp_server, 21, ftp_user, ftp_pwd, banner_timeout=2000)

        #     # ftp_client = ssh_client.open_sftp()

        #     # list_files = ftp_client.listdir(ftp_path_out)

        #     _logger.info("""

        #             connect in try

        #             """)

        # except:
        #     _logger.info("""

        #             ERROR

        #             """)

        # else:
        #     _logger.info("""

        #             connect in else

        #             """)

        # Hostname = "remote-ip-address"
        # Username = "root"
        # Password = "password"

        with pysftp.Connection(host=ftp_server, username=ftp_user, password=ftp_pwd) as sftp:
            _logger.info("""
                         
                         
                         
                         Connection successfully established ... 
                         
                         
                         
                         """)

            # # Define a file that you want to upload from your local directory
            # localFilePath = '/boot/initrd.img'

            # # Define the remote path where the file will be uploaded
            # remoteFilePath = '/mnt/initrd.img'

            # Use put method to upload a file
            sftp.put('./', ftp_pwd)

            # Switch to a remote directory
            sftp.cwd(ftp_pwd)

            # Obtain structure of the remote directory '/opt'
            directory_structure = sftp.listdir_attr()

            # Print data
            for attr in directory_structure:
                _logger.info(f"""
                             
                             
                             {attr.filename}
                             {attr}
                             
                             
                             
                             """)

        return super(SaleOrder, self).create(vals)
