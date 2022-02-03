from odoo import api, fields, models
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)


class ProductWishlist(models.Model):

    _inherit = "product.wishlist"


    @api.model
    def current(self):
        """Get all wishlist items that belong to current user or session,
        filter products that are unpublished."""
        if not request:
            return self

        if request.website.is_public_user():
            wish = self.sudo().search([('id', 'in', request.session.get('wishlist_ids', []))])
        else:
            wish = self.search([("partner_id", "=", self.env.user.partner_id.id), ('website_id', '=', request.website.id)])
        
        partner = self.env.user.partner_id
        if partner:
            if partner.nxt_is_b2b:
                values_ids = []
                for rec_wish in wish:
                    values_ids.append(rec_wish.product_id.id)
                products_b2b = request.env["product.product"].sudo().search([
                    ("special_category.name","=",partner.nxt_id_erp),
                    ("is_published","=",True),
                ])
                if products_b2b:
                    _logger.info("get_wishlist  values_ids:" + str(values_ids))
                    for product in products_b2b:
                        if product.id not in values_ids:
                            _logger.info("get_wishlist  product.id:" + str(product.id))
                            request.env["product.wishlist"].sudo().create({"partner_id":partner.id, "website_id":request.website.id, "product_id":product.id})
                    
                    wish = self.search([("partner_id", "=", partner.id), ('website_id', '=', request.website.id)])

        return wish.filtered(lambda x: x.sudo().product_id.product_tmpl_id.website_published and x.sudo().product_id.product_tmpl_id.sale_ok)