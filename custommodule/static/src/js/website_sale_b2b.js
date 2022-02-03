odoo.define('custommodule.website_sale_b2b', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
var VariantMixin = require('sale.VariantMixin');
require('website_sale.website_sale');

    publicWidget.registry.CustomWebSiteSaleB2B = publicWidget.Widget.extend({
        selector: '.oe_website_sale',
        events: {
            'change input[name="first_name"]': '_onChangeNames',
            'change input[name="last_name"]': '_onChangeNames',
            'click .a-submit-fiscal-info': '_onClickSubmitFiscallInfo',
            'submit .a-submit-fiscal-info': '_onClickSubmitFiscallInfo'
            //'submit .checkout_autoformat': '_clickSubmit',
            //'click .checkout_autoformat .btn-primary': '_clickSubmit'
        },
        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------
        /**
         * @private
         * @param {Event} ev
         */
        _onChangeNames: function (ev) {

            var $input = $(ev.currentTarget);
            var $first_name = $('input[name="first_name"]');
            var $last_name = $('input[name="last_name"]');

            var first_name = $first_name.val();
            if(first_name.toUpperCase() !== $first_name.val()){
                $first_name.val(first_name.toUpperCase())
            }

            var last_name = $last_name.val();
            if(last_name.toUpperCase() !== $last_name.val()){
                $last_name.val(last_name.toUpperCase())
            }

            var $name = $('input[name="name"]');
            var fullname = $last_name.val() + (String($first_name.val()).length>0?" ":"") + $first_name.val(); 
            console.info(fullname);
            $name.val(fullname);
        },
        disableButton: function (button) {
            if (!$(button).attr('disabled')){
                $(button).attr('disabled', true);
                $(button).children('.fa-lock').removeClass('fa-lock');
                $(button).prepend('<span class="o_loader"><i class="fa fa-refresh fa-spin"></i>&nbsp;</span>');
            }
        },
    
        enableButton: function (button) {
            if ($(button).attr('disabled')){
                $(button).attr('disabled', false);
                $(button).children('.fa').addClass('fa-lock');
                $(button).find('span.o_loader').remove();
            }
        },
        /**
         * @private
         * @param {Event} ev
         * @returns {Promise}
         */
        _submitCode: function (ev) {
            if (ev.type === 'submit') {
                var button = $('#btn-primary');
            } else {
                var button = ev.target;
            }
            
            var $aSubmit = $(ev.currentTarget);
            this.disableButton(button);
            var modeaddress = $('#modeaddress').val();
            if(modeaddress !== "billing"){
                $aSubmit.closest('form').submit();
                return;
            }

            console.info("button",button);
            var $input = $(ev.currentTarget);
            var $vat = $('input[name="vat"]');
            var $identification_type_id = $("select[name='identification_type_id'] option:selected");
            var $last_name = $('input[name="last_name"]');
            var $first_name = $('input[name="first_name"]');
            var $name = $('input[name="name"]');
            var $vat = $('input[name="vat"]');
            var $phone = $('input[name="phone"]');
            
            var identification_type_id = $identification_type_id.data("name");
            var last_name = $last_name.val();
            var first_name = $first_name.val();
            var name = $name.val();
            var vat = $vat.val();
            var phone = $phone.val();

            console.info("identification_type_id",identification_type_id);
            console.info("first_name",first_name);
            console.info("last_name",last_name);
            console.info("name",name);
            console.info("vat",vat);
            var flagError = false;
            if(String(name).length == 0 ){
                flagError = true;
                alert("Debe ingresar el campo >> Nombre completo/Razón Social");
                this.enableButton(button);
                return;
            }

            if(String(phone).length == 0 ){
                flagError = true;
                alert("Debe ingresar el campo Telefono");
                this.enableButton(button);
                return;
            }

            if(String(first_name).length == 0 && identification_type_id == "CI"){
                flagError = false;
                alert("Debe ingresar el campo >> Nombres");
                this.enableButton(button);
                return;
            }

            if(String(last_name).length == 0 && identification_type_id == "CI"){
                flagError = true;
                alert("Debe ingresar el campo >> Apellidos");
                this.enableButton(button);
                return;
            }

            if(identification_type_id == "CI"  && String(vat).length != 10){
                flagError = true;
                alert("Número de Cédula incorrecto!");
                this.enableButton(button);
                return;
            }
            
            if((identification_type_id == "RUC-PN" || identification_type_id == "RUC-PJ" )  && String(vat).length != 13){
                alert("Número de RUC incorrecto!");
                flagError = true;
                this.enableButton(button);
                return;
            }

            if(!flagError){
                $aSubmit.closest('form').submit();
            }
            
        },
        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------
        /**
         * @private
         * @param {Event} ev
         */
        _onClickSubmitFiscallInfo: function (ev) {
            if (!ev.isDefaultPrevented()) {
                ev.preventDefault();
                
                this._submitCode(ev);
            }
        }
        
        /**
         * @private
         * @param {Event} ev
         */
        /*
        ,_onClickSubmitFiscallInfo: function (ev, forceSubmit) {
            if ($(ev.currentTarget).is('#add_to_cart, #products_grid .a-submit') && !forceSubmit) {
                return;
            }
            var $aSubmit = $(ev.currentTarget);
            if (!ev.isDefaultPrevented() && !$aSubmit.is(".disabled")) {
                ev.preventDefault();
                $aSubmit.closest('form').submit();
            }
            if ($aSubmit.hasClass('a-submit-disable')){
                $aSubmit.addClass("disabled");
            }
            if ($aSubmit.hasClass('a-submit-loading')){
                var loading = '<span class="fa fa-cog fa-spin"/>';
                var fa_span = $aSubmit.find('span[class*="fa"]');
                if (fa_span.length){
                    fa_span.replaceWith(loading);
                } else {
                    $aSubmit.append(loading);
                }
            }
        }*/
    });


});