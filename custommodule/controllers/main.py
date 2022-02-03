# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import logging
from datetime import datetime
from werkzeug.exceptions import Forbidden, NotFound


import odoo
from odoo.tools import image_process, topological_sort, html_escape, pycompat, ustr, apply_inheritance_specs, lazy_property, float_repr
from odoo import fields, http, modules, tools, _
from odoo.http import request
from odoo.addons.base.models.ir_qweb_fields import nl2br
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.exceptions import ValidationError
from odoo.osv import expression
from odoo.addons.website_form.controllers.main import WebsiteForm
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.main import TableCompute
from odoo.addons.website.controllers.main import Website
from odoo.tools.mimetypes import guess_mimetype
from odoo.modules import get_module_path, get_resource_path

import base64
import io

_logger = logging.getLogger(__name__)


class CustomWebsiteSale(WebsiteSale):

    @http.route(['/shop/quote/presentacion'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def shop_quote_presentacion(self, product_id):
        _logger.error("product_id :" + str(product_id))
        list_values = []
        presentaciones = request.env["custommodule.quote.products"].sudo().search([
            ("product_tmpl_id.id","=",product_id)
        ])
        _logger.error(" presentaciones:" + str(presentaciones))
        for presentacion in presentaciones:
            list_temp = {"name":presentacion.quote_size.name
            , "id":presentacion.quote_size.id}
            if list_temp not in list_values:
                list_values.append(list_temp)
        _logger.error("list_values presentacion:" + str(list_values))
        return list_values
        

    @http.route(['/shop/quote/cantidad'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def shop_quote_cantidad(self, presentacion_id, product_id):
        _logger.error("presentacion_id:" + str(presentacion_id))
        _logger.error("product_id :" + str(product_id))

        list_values = []
        cantidades = request.env["custommodule.quote.products"].sudo().search([
            ("product_tmpl_id.id","=",product_id),
            ("quote_size.id","=",presentacion_id),
        ])
        for cantidad in cantidades:
            list_temp = {"name":cantidad.quote_quantity.name
            , "id":cantidad.quote_quantity.id}
            if list_temp not in list_values:
                list_values.append(list_temp)
        _logger.error("list_values cantidad:" + str(list_values))
        return list_values
    
    @http.route(['/shop/quote/form_save'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def shop_quote_form_save(self, item_list
        , primer_nombre=None, segundo_nombre=None, phone=None, email=None, tipo_documento=None, vat=None, name=None
        , calle_billing=None, state_id=None, city_id=None
        , list_delivery=None, calle_delivery=None, state_id_delivery=None, city_id_delivery=None
        ):
        _logger.error("item_list:" + str(item_list))
        partner_id = request.env.user.partner_id.id
        partner_delivery_id = partner_id
        is_public_user = request.env.user.has_group('base.group_public')

        full_name =  name.strip()
        vals_billing = {
            'name': full_name.strip(),
            'primer_nombre':primer_nombre.strip(),
            'segundo_nombre': segundo_nombre.strip(),
            'vat': vat.strip(),
            'phone': phone,
            'email': email,
            'street': calle_billing,
            'state_id': int(state_id),
            'city_id': int(city_id),
        }

        vals_delivery = {
            'name': "DIR_ENTREGA_1",
            'phone': phone,
            'email': email,
            'street': calle_delivery,
            'state_id': int(state_id_delivery),
            'city_id': int(city_id_delivery),
            'parent_id': int(partner_id),
            'type': 'delivery',
        }

        if is_public_user:
            partner_obj = request.env["res.partner"]
            partner = partner_obj.sudo().create(vals_billing)
            partner_id = partner.id
            partner_delivery_id = partner_id

            if int(list_delivery) == -1:
                vals_delivery.update(parent_id=int(partner_id))
                partner_delivery = partner_obj.sudo().create(vals_delivery)
                partner_delivery_id = partner_delivery.id
        else:
            partner_obj = request.env["res.partner"]
            partner = partner_obj.sudo().browse(partner_id)
            partner.sudo().write(vals_billing)
            
            if int(list_delivery) == -1:
                list_delivery = partner_obj.sudo().search([("parent_id","=",int(partner_id)), ("type","=","delivery")])
                vals_delivery.update(
                    parent_id=int(partner_id),
                    name="DIR_ENTREGA_" + str(int(list_delivery)),
                )
                partner_delivery = partner_obj.sudo().create(vals_delivery)
                partner_delivery_id = partner_delivery.id

            if int(list_delivery) > 1:
                partner_delivery = partner_obj.sudo().browse(int(list_delivery))
                vals_delivery.pop("parent_id")
                partner_delivery.sudo().write(vals_delivery)
                partner_delivery_id = partner_delivery.id



        sale_order = request.env["sale.order"].sudo().create({
            "partner_id":int(partner_id),
            "partner_shipping_id":int(partner_delivery_id),
            "user_id":2, # VENTAS   
            "is_quote":True,
            "date_order":datetime.today()
        })
        _logger.error("sale_order cotizacion:" + str(sale_order.name))
        for data in item_list:
            _logger.error("sale_order data:" + str(data))
            _logger.error("sale_order qty_id:" + str(data.get('qty_id')))
            _logger.error("sale_order present_id:" + str(data.get('present_id')))
            _logger.error("sale_order item:" + str(data.get('item')))
            present_id = data.get('present_id')
            qty_id = data.get('qty_id')
            item_id = data.get('item')
            #domain = request.env["product.template.attribute.value"].sudo().search([('id', 'in',[qty_id,present_id])])
            product_id = request.env['custommodule.quote.products'].sudo().search([
                ("quote_size.id","=",present_id),
                ("quote_quantity.id","=",qty_id),
                ('product_tmpl_id.id', '=', item_id)
            ], limit = 1)
            if product_id:
                description = (
                    product_id.product_tmpl_id.name 
                    + " - " + product_id.quote_size.name + " - (" + str((product_id.quote_quantity.name/product_id.quote_unit_case))
                    + " Caja(s)/ " + str(product_id.quote_unit_case) + " Und)"
                )

                request.env['sale.order.line'].sudo().create({
                    #'product_id': product_id.product_variant_id.id,
                    'product_id': product_id.product_tmpl_id.product_variant_id.id,
                    'order_id': sale_order.id,
                    'name': description,
                    'quote_size': product_id.quote_size.name,
                    'quote_quantity': product_id.quote_quantity.name,
                    'quote_id_erp': product_id.id_erp,
                    'product_uom_qty': product_id.quote_quantity.name,
                    'price_unit': product_id.quote_price,
                })
        
        sale_order.sudo().action_quotation_sent()
        
        template = request.env['mail.template'].sudo().browse(11)
        if template:
            template.send_mail(sale_order.id, email_values={'email_to': email})
            
            #sale_order.sudo().write({"state":'sent'})"""
        return sale_order.name

    @http.route(['/shop/select_payment_website'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def select_payment_website(self, acquirer_id):
        order = request.website.sale_get_order(force_create=1)
        _logger.error("acquirer_id 1 :" + str(acquirer_id))
        _logger.error("order.state :" + str(order.state))
        if order.state != 'draft':
            request.website.sale_reset()
            return {}
        
        _logger.error("order :" + str(order.name))
        _logger.error("acquirer_id :" + str(acquirer_id))
        if acquirer_id is not False and order.payment_web_site.id != acquirer_id :
            order.sudo().write({"payment_web_site":str(acquirer_id)})
            _logger.error("payment_web_site :" + str(order.payment_web_site))


    def _checkout_form_save(self, mode, checkout, all_values):
        res = super(CustomWebsiteSale, self)._checkout_form_save(mode, checkout, all_values)
        partnerId = int(all_values.get('partner_id', -1))
        if partnerId == -1:
            partnerObj = request.env['res.partner'].sudo().browse(res)
            if 'submitted' in all_values:
                self.updateInformation(partnerObj, all_values)
        return res

    @http.route(['/shop/quick_add_item'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def quick_add_item(self, product_id, add_qty=1, set_qty=0, **kw):
        """This route is called when adding a product to cart (no options)."""
        sale_order = request.website.sale_get_order(force_create=True)
        if sale_order.state != 'draft':
            request.session['sale_order_id'] = None
            sale_order = request.website.sale_get_order(force_create=True)

        product_custom_attribute_values = None
        if kw.get('product_custom_attribute_values'):
            product_custom_attribute_values = json.loads(kw.get('product_custom_attribute_values'))

        no_variant_attribute_values = None
        if kw.get('no_variant_attribute_values'):
            no_variant_attribute_values = json.loads(kw.get('no_variant_attribute_values'))

        _logger.error("quick_add after _cart_update :" + str(product_id))
        sale_order._cart_update(
            product_id=int(product_id),
            add_qty=add_qty,
            set_qty=set_qty,
            product_custom_attribute_values=product_custom_attribute_values,
            no_variant_attribute_values=no_variant_attribute_values
        )
        _logger.error("quick_add before _cart_update :" + str(product_id))

        website_sale_order = request.website.sale_get_order()
        _logger.error("website_sale_order.cart_quantity :" + str(website_sale_order.cart_quantity))
        value = {}
        value["website_sale.cart_quantity"] = website_sale_order.cart_quantity if website_sale_order.cart_quantity else ''
        _logger.error("website_sale[] :" + str(value))
        return value

    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True, sitemap= WebsiteSale.sitemap_shop)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        add_qty = int(post.get('add_qty', 1))
        Category = request.env['product.public.category']
        if category:
            category = Category.search([('id', '=', int(category))], limit=1)
            if not category or not category.can_access_from_current_website():
                raise NotFound()
        else:
            category = Category

        if ppg:
            try:
                ppg = int(ppg)
                post['ppg'] = ppg
            except ValueError:
                ppg = False
        if not ppg:
            ppg = request.env['website'].get_current_website().shop_ppg or 20

        ppr = request.env['website'].get_current_website().shop_ppr or 4

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attributes_ids = {v[0] for v in attrib_values}
        attrib_set = {v[1] for v in attrib_values}

        domain = self._get_search_domain(search, category, attrib_values)

        keep = QueryURL('/shop', category=category and int(category), search=search, attrib=attrib_list, order=post.get('order'))

        pricelist_context, pricelist = self._get_pricelist_context()

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

        url = "/shop"
        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        Product = request.env['product.template'].with_context(bin_size=True)
        #PERSONALIZACION PARA QUE SOLO TRAIGA LOS ITEMS DE LA LISTA DE PRECIOS
        list_items = []
        _logger.error("pricelist :" + str(pricelist.id) + "  item.name :" + str(pricelist.name))
        for item in pricelist.item_ids:
            list_items.append(item.product_tmpl_id.id)
        items_pricelist_domain = [('id', 'in', list_items)]

        domain += items_pricelist_domain
        #PERSONALIZACION PARA CATEGORIAS ESPECIALES
        list_special_category_partner_ids = []
        for special_category_partner_ids in request.env.user.partner_id.special_category:
            list_special_category_partner_ids.append(special_category_partner_ids.id)
        items_special_category = [('special_category', 'in', list_special_category_partner_ids)]
        #SE VALIDA QUE TENGA AL MENOS UNA CATEGORIA PARA EL CASO DE USUARIO PUBLICO
        if len(list_special_category_partner_ids) > 0:
            domain += items_special_category

        _logger.error("domain :" + str(domain))
        search_product = Product.search(domain)
        website_domain = request.website.website_domain()
        categs_domain = [('parent_id', '=', False)] + website_domain
        if search:
            search_categories = Category.search([('product_tmpl_ids', 'in', search_product.ids)] + website_domain).parents_and_self
            categs_domain.append(('id', 'in', search_categories.ids))
        else:
            search_categories = Category
        categs = Category.search(categs_domain)

        if category:
            url = "/shop/category/%s" % slug(category)

        product_count = len(search_product)
        pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        products = Product.search(domain, limit=ppg, offset=pager['offset'], order=self._get_search_order(post))

        ProductAttribute = request.env['product.attribute']
        if products:
            # get all products without limit
            attributes = ProductAttribute.search([('product_tmpl_ids', 'in', search_product.ids)])
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        layout_mode = request.session.get('website_sale_shop_layout_mode')
        if not layout_mode:
            if request.website.viewref('website_sale.products_list_view').active:
                layout_mode = 'list'
            else:
                layout_mode = 'grid'

        values = {
            'search': search,
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'pricelist': pricelist,
            'add_qty': add_qty,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg, ppr),
            'ppg': ppg,
            'ppr': ppr,
            'categories': categs,
            'attributes': attributes,
            'keep': keep,
            'search_categories_ids': search_categories.ids,
            'layout_mode': layout_mode,
        }
        if category:
            values['main_object'] = category
        return request.render("website_sale.products", values)

    # --------------------------------------------------------------------------
    # Products Search Bar
    # --------------------------------------------------------------------------

    @http.route('/shop/products/autocomplete', type='json', auth='public', website=True)
    def products_autocomplete(self, term, options={}, **kwargs):
        """
        Returns list of products according to the term and product options

        Params:
            term (str): search term written by the user
            options (dict)
                - 'limit' (int), default to 5: number of products to consider
                - 'display_description' (bool), default to True
                - 'display_price' (bool), default to True
                - 'order' (str)
                - 'max_nb_chars' (int): max number of characters for the
                                        description if returned

        Returns:
            dict (or False if no result)
                - 'products' (list): products (only their needed field values)
                        note: the prices will be strings properly formatted and
                        already containing the currency
                - 'products_count' (int): the number of products in the database
                        that matched the search query
        """
        ProductTemplate = request.env['product.template']

        display_description = options.get('display_description', True)
        display_price = options.get('display_price', True)
        order = self._get_search_order(options)
        max_nb_chars = options.get('max_nb_chars', 999)

        category = options.get('category')
        attrib_values = options.get('attrib_values')

        domain = self._get_search_domain(term, category, attrib_values, display_description)
        
        #PERSONALIZACION PARA QUE SOLO TRAIGA LOS ITEMS DE LA LISTA DE PRECIOS
        pricelist_context, pricelist = self._get_pricelist_context()
        list_items = []
        for item in pricelist.item_ids:
            list_items.append(item.product_tmpl_id.id)
        items_pricelist_domain = [('id', 'in', list_items)]

        domain += items_pricelist_domain
        #PERSONALIZACION PARA CATEGORIAS ESPECIALES
        list_special_category_partner_ids = []
        for special_category_partner_ids in request.env.user.partner_id.special_category:
            list_special_category_partner_ids.append(special_category_partner_ids.id)
        items_special_category = [('special_category', 'in', list_special_category_partner_ids)]
        #SE VALIDA QUE TENGA AL MENOS UNA CATEGORIA PARA EL CASO DE USUARIO PUBLICO
        if len(list_special_category_partner_ids) > 0:
            domain += items_special_category

        _logger.error("domain :" + str(domain))

        products = ProductTemplate.search(
            domain,
            limit=min(20, options.get('limit', 5)),
            order=order
        )

        fields = ['id', 'name', 'website_url']
        if display_description:
            fields.append('description_sale')

        res = {
            'products': products.read(fields),
            'products_count': ProductTemplate.search_count(domain),
        }

        if display_description:
            for res_product in res['products']:
                desc = res_product['description_sale']
                if desc and len(desc) > max_nb_chars:
                    res_product['description_sale'] = "%s..." % desc[:(max_nb_chars - 3)]

        if display_price:
            FieldMonetary = request.env['ir.qweb.field.monetary']
            monetary_options = {
                'display_currency': request.website.get_current_pricelist().currency_id,
            }
            for res_product, product in zip(res['products'], products):
                combination_info = product._get_combination_info(only_template=True)
                res_product.update(combination_info)
                res_product['list_price'] = FieldMonetary.value_to_html(res_product['list_price'], monetary_options)
                res_product['price'] = FieldMonetary.value_to_html(res_product['price'], monetary_options)

        return res

    #VALORES POR DEFECTO EN CLIENTES NUEVOS - MEJORA DE LISTA DE PRECIOS
    def values_postprocess(self, order, mode, values, errors, error_msg):
        new_values = {}
        authorized_fields = request.env['ir.model']._get('res.partner')._get_form_writable_fields()
        for k, v in values.items():
            # don't drop empty value, it could be a field to reset
            if k in authorized_fields and v is not None:
                new_values[k] = v
            else:  # DEBUG ONLY
                if k not in ('field_required', 'partner_id', 'callback', 'submitted'): # classic case
                    _logger.debug("website_sale postprocess: %s value has been dropped (empty or not writable)" % k)

        new_values['team_id'] = request.website.salesteam_id and request.website.salesteam_id.id
        new_values['user_id'] = request.website.salesperson_id and request.website.salesperson_id.id

        if request.website.specific_user_account:
            new_values['website_id'] = request.website.id

        if mode[0] == 'new':
            new_values['company_id'] = request.website.company_id.id
            if request.website.default_pricelist_id :
                new_values['property_product_pricelist'] = request.website.default_pricelist_id.id
                
        lang = request.lang.code if request.lang.code in request.website.mapped('language_ids.code') else None
        if lang:
            new_values['lang'] = lang
        if mode == ('edit', 'billing') and order.partner_id.type == 'contact':
            new_values['type'] = 'other'
        if mode[1] == 'shipping':
            new_values['parent_id'] = order.partner_id.commercial_partner_id.id
            new_values['type'] = 'delivery'

        return new_values, errors, error_msg



    @http.route(['/shop/wishlist'], type='http', auth="public", website=True, sitemap=False)
    def get_wishlist(self, count=False, **kw):
        partner = request.env.user.partner_id
        values = request.env['product.wishlist'].with_context(display_default_code=False, partner=partner).current()
        
        if count:
            return request.make_response(json.dumps(values.mapped('product_id').ids))

        if not len(values):
            return request.redirect("/shop")

        return request.render("website_sale_wishlist.product_wishlist", dict(wishes=values))

    @http.route([
        '/imagen_producto/<int:product_id>',
    ], type='http', auth="public")
    def imagen_producto(self, product_id, **kw):
        imgname = 'logo'
        imgext = '.png'

        product = request.env["product.template"].sudo().browse(product_id)
        image_base64 = None
        if product["image_128"]:
            image_base64 = product["image_128"]
            
        width=0 
        height=0
        status = 200
        if not (width or height):
            width, height = odoo.tools.image_guess_size_from_field_name("image_128")

        if not image_base64:
            with tools.file_open(get_resource_path('web', 'static/src/img', 'placeholder.png'), 'rb') as fd:
                image_base64 = base64.b64encode(fd.read()) 
        try:
            image_base64 = image_process(image_base64, size=(int(width), int(height)), crop=False, quality=int(0))
        except Exception as e:
            _logger.info("imagen_producto error: %s " % e)
            return request.not_found()

        headers = [('Content-Type', "image/png"), ('X-Content-Type-Options', 'nosniff')]
        content = base64.b64decode(image_base64)
        headers = http.set_safe_image_headers(headers, content)
        response = request.make_response(content, headers)
        response.status_code = status
        return response
