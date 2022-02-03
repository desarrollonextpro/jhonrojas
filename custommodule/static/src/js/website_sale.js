odoo.define('custommodule.website_sale', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
var VariantMixin = require('sale.VariantMixin');
require('website_sale.website_sale');


publicWidget.registry.CustomPaymentSelectList = publicWidget.Widget.extend({
    selector: '.o_payment_acquirer_select',
    start: function () {

        var $input_select_payment_method = $('.o_payment_acquirer_select input[type="radio"]:checked').first();
        if($input_select_payment_method.prop( "checked" ) == true){
            $input_select_payment_method.trigger('change');
            console.log("init value payment",$input_select_payment_method);
        }
        $("#o_payment_form_pay").attr('disabled', true);
        return this._super.apply(this, arguments);
    },
});

publicWidget.registry.CustomWebSiteSale = publicWidget.Widget.extend({
    selector: '.oe_website_sale',
    events: {
        //'click .o_wsale_product_btn .add-qcky-submit': '_onClickQuickAdd'
    },
    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------
    /**
     * @private
     * @param {Event} ev
     */
    _onClickQuickAdd: function (ev) {

        var $input = $(ev.currentTarget);
        var product_id = $input.data("product-id");

        console.log("product_id", product_id);
        
        console.log("Entro quick add");
        this._rpc({
            route: "/shop/quick_add_item",
            params: {
                product_id: product_id
            },
        }).then(function (data) {
            console.log("data", data);
            console.log("Actual value", $(".my_cart_quantity").first().text());
            $(".my_cart_quantity").html(data['website_sale.cart_quantity']).hide().fadeIn(600);
            console.log("Set value", data['website_sale.cart_quantity']);
            if($(".o_wsale_my_cart").hasClass("d-none")){
                $(".o_wsale_my_cart").removeClass("d-none");
            };
            $("#item_check_quick_add_"+product_id).removeClass("d-none");
        });
    }
});

publicWidget.registry.CustomPaymentForm = publicWidget.Widget.extend({
    selector: '.o_payment_form',
    events: {
        'click .o_payment_acquirer_select': 'radioClickEvent',
        'change .o_payment_acquirer_select': 'radioClickEvent',
        'change #checkbox_cgv': '_aceptTerms',
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @private
     * @param {Event} ev
     */
     _aceptTerms: function (ev) {
        console.log("_aceptTerms o_payment_form_pay ",$('#checkbox_cgv').prop( "checked" ));
        
        //ev.preventDefault();
        var nxt_is_b2b = $('#nxt_is_b2b').val();
        if (nxt_is_b2b == "True")
        {
            ev.stopPropagation();
            console.info("nxt_is_b2b:", nxt_is_b2b);
            if ($('#checkbox_cgv').prop( "checked" )) {
                $("#o_payment_form_pay").attr('disabled', false);
            }else{
                $("#o_payment_form_pay").attr('disabled', true);
            };
        }
    },

    /**
     * @private
     */
    updateNewPaymentDisplayStatus: function () {
        var checked_radio = this.$('input[type="radio"]:checked');
        // we hide all the acquirers form
        this.$('[id*="o_payment_add_token_acq_"]').addClass('d-none');
        this.$('[id*="o_payment_form_acq_"]').addClass('d-none');
        if (checked_radio.length !== 1) {
            return;
        }
        checked_radio = checked_radio[0];
        var acquirer_id = this.getAcquirerIdFromRadio(checked_radio);
        console.info("acquirer_id:", acquirer_id);
        this._rpc({
            route: "/shop/select_payment_website",
            params: {
                acquirer_id: acquirer_id
            },
        });

        // if we clicked on an add new payment radio, display its form
        if (this.isNewPaymentRadio(checked_radio)) {
            this.$('#o_payment_add_token_acq_' + acquirer_id).removeClass('d-none');
        }
        else if (this.isFormPaymentRadio(checked_radio)) {
            this.$('#o_payment_form_acq_' + acquirer_id).removeClass('d-none');
        }
    },
    /**
     * @private
     * @param {DOMElement} element
     */
    getAcquirerIdFromRadio: function (element) {
        return $(element).data('acquirer-id');
    }
    ,
    /**
     * @private
     * @param {DOMElement} element
     */
    isFormPaymentRadio: function (element) {
        return $(element).data('form-payment') === 'True';
    },
    /**
     * @private
     * @param {DOMElement} element
     */
    isNewPaymentRadio: function (element) {
        return $(element).data('s2s-payment') === 'True';
    },
    /**
     * Called when clicking on a radio button.
     *
     * @private
     * @param {Event} ev
     */
    radioClickEvent: function (ev) {
        // radio button checked when we click on entire zone(body) of the payment acquirer
        $(ev.currentTarget).find('input[type="radio"]').prop("checked", true);
        this.updateNewPaymentDisplayStatus();
    }
});

});