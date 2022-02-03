odoo.define('custommodule.website_sale_quote', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
var VariantMixin = require('sale.VariantMixin');
require('website_sale.website_sale');

    publicWidget.registry.CustomWebSiteSaleQuote = publicWidget.Widget.extend({
        selector: '.oe_website_sale_quote',
        events: {
            'change #selectproduct': '_onChangeSelectProduct',
            'change #selectpresentacion': '_onChangeSelectPresentacion',
            'click #btn-add-item': '_onClickAddItem',
            'click .js_delete_item_quote': '_onClickDeleteItem',
            'click .o_website_form_send_quote': '_onClickSend',
            'change input[name="primer_nombre"]': '_onChangeNames',
            'change input[name="segundo_nombre"]': '_onChangeNames',
            'change input[name="name"]': '_onChangeRazonSocial',
            'change input[name="calle_billing"]': '_onChangeCalleBilling',
            'change input[name="calle_delivery"]': '_onChangeCalleDelivery',
            'change select[name="state_id"]': '_onChangeState',
            'change select[name="state_id_delivery"]': '_onChangeStateDelivery',
            'change select[name="list_delivery"]': '_onChangeListDelivery',
        },
        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------
        /**
         * @private
         * @param {Event} ev
         */
         _onChangeNames: function (ev) {

            var $input = $(ev.currentTarget);
            var $primer_nombre = $('input[name="primer_nombre"]');
            var $segundo_nombre = $('input[name="segundo_nombre"]');

            var primer_nombre = $primer_nombre.val();
            if(primer_nombre.toUpperCase() !== $primer_nombre.val()){
                $primer_nombre.val(primer_nombre.toUpperCase())
            }

            var segundo_nombre = $segundo_nombre.val();
            if(segundo_nombre.toUpperCase() !== $segundo_nombre.val()){
                $segundo_nombre.val(segundo_nombre.toUpperCase())
            }

            var $name = $('input[name="name"]');
            var fullname = $segundo_nombre.val() + (String($primer_nombre.val()).length>0?" ":"") + $primer_nombre.val(); 
            console.info(fullname);
            $name.val(fullname);

        },
        _onChangeRazonSocial: function (ev) {

            var $input = $(ev.currentTarget);
            var $name = $('input[name="name"]');

            var name = $name.val();
            if(name.toUpperCase() !== $name.val()){
                $name.val(name.toUpperCase())
            }
        },
        _onChangeCalleBilling: function (ev) {

            var $input = $(ev.currentTarget);
            var $name = $('input[name="calle_billing"]');

            var name = $name.val();
            if(name.toUpperCase() !== $name.val()){
                $name.val(name.toUpperCase())
            }
        },
        _onChangeCalleDelivery: function (ev) {

            var $input = $(ev.currentTarget);
            var $name = $('input[name="calle_delivery"]');

            var name = $name.val();
            if(name.toUpperCase() !== $name.val()){
                $name.val(name.toUpperCase())
            }
        },
        /**
         * @private
         * @param {Event} ev
         */
         _onChangeState: function (ev) {
            //if (!this.$('.checkout_autoformat').length) {
            //    return;
            //}
            this._changeState();
        },
        /**
         * @private
         */
         _changeState: function () {
            console.log('$("#state_id").val()', $("#state_id").val());
            if (!$("#state_id").val() || $("#state_id").val()=="0" ) {
                var selectCities = $("select[name='city_id']");
                selectCities.html('');
                var opt = $('<option>').text('Ciudad..')
                        .attr('value', '');
                selectCities.append(opt);
                selectCities.parent('div').show();
                selectCities.data('init', 0);
                return;
            }
            this._rpc({
                route: "/shop/cities_infos/" + $("#state_id option:selected").val(),
                params: {
                    mode:'shipping'
                },
            }).then(function (array_data) {
                // placeholder phone_code
                //$("input[name='phone']").attr('placeholder', data.phone_code !== 0 ? '+'+ data.phone_code : '');

                // populate states and display
                var selectCities = $("select[name='city_id']");
                // dont reload state at first loading (done in qweb)
                if (selectCities.data('init')===0 || selectCities.find('option').length===1) {
                    if (array_data.length) {
                        console.log('array_data', array_data);
                        selectCities.html('');
                        var opt = $('<option>').text('Ciudad..')
                                .attr('value', '0');
                            selectCities.append(opt);

                        _.each(array_data, function (x) {
                            var opt = $('<option>').text(x.name)
                                .attr('value', x.id);
                            selectCities.append(opt);
                        });
                        selectCities.parent('div').show();
                    } else {
                        selectCities.val('').parent('div').hide();
                        
                    }
                    selectCities.data('init', 0);
                } else {
                    selectCities.data('init', 0);
                }

                // manage fields order / visibility
                if (array_data.fields) {
                    _.each(all_fields, function (field) {
                        $(".checkout_autoformat .div_" + field.split('_')[0]).toggle($.inArray(field, data.fields)>=0);
                    });
                }
            });
        },
        /**
         * @private
         */
        _onChangeListDelivery: function () {
            console.log('$("#list_delivery").val()', $("#list_delivery").val());
            if (!$("#list_delivery").val()) {
                return;
            }
            
            var $list_delivery = $("#list_delivery option:selected");
            var street = $list_delivery.data("street");
            var state_id = $list_delivery.data("state_id");
            var city_id = $list_delivery.data("city_id");
            var $calle_delivery = $('input[name="calle_delivery"]');

            $("#state_id_delivery  option:selected").removeAttr("selected");
            $("#city_id_delivery  option:selected").removeAttr("selected");
            
            $calle_delivery.val(street);
            $('#state_id_delivery option[value='+state_id+']').attr("selected", true);
            this._changeStateDelivery();
            $('#city_id_delivery option[value='+city_id+']').attr("selected", true).change();;

        },
        /**
         * @private
         * @param {Event} ev
         */
         _onChangeStateDelivery: function (ev) {
            //if (!this.$('.checkout_autoformat').length) {
            //    return;
            //}
            this._changeStateDelivery();
        },
        /**
         * @private
         */
         _changeStateDelivery: function () {
            console.log('$("#state_id_delivery").val()', $("#state_id_delivery").val());
            if (!$("#state_id_delivery").val() || $("#state_id_delivery").val()=="0" ) {
                var selectCities = $("select[name='city_id_delivery']");
                selectCities.html('');
                var opt = $('<option>').text('Ciudad..')
                        .attr('value', '0');
                selectCities.append(opt);
                selectCities.parent('div').show();
                selectCities.data('init', 0);
                return;
            }
            this._rpc({
                route: "/shop/cities_infos/" + $("#state_id_delivery option:selected").val(),
                params: {
                    mode:'shipping'
                },
            }).then(function (array_data) {
                // placeholder phone_code
                //$("input[name='phone']").attr('placeholder', data.phone_code !== 0 ? '+'+ data.phone_code : '');

                // populate states and display
                var selectCities = $("select[name='city_id_delivery']");
                // dont reload state at first loading (done in qweb)
                if (selectCities.data('init')===0 || selectCities.find('option').length===1) {
                    if (array_data.length) {
                        console.log('array_data', array_data);
                        selectCities.html('');

                        var $list_delivery = $("#list_delivery option:selected");
                        var city_id = $list_delivery.data("city_id");
                        
                        var opt = $('<option>').text('Ciudad..')
                                .attr('value', '0');
                            selectCities.append(opt);

                        _.each(array_data, function (x) {
                            var opt = $('<option>').text(x.name)
                                .attr('value', x.id);
                            if (x.id == city_id) {
                                opt.attr("selected", true);
                            }
                            selectCities.append(opt);
                        });
                        selectCities.parent('div').show();
                    } else {
                        selectCities.val('').parent('div').hide();
                        
                    }
                    selectCities.data('init', 0);
                } else {
                    selectCities.data('init', 0);
                }

                // manage fields order / visibility
                if (array_data.fields) {
                    _.each(all_fields, function (field) {
                        $(".checkout_autoformat .div_" + field.split('_')[0]).toggle($.inArray(field, data.fields)>=0);
                    });
                }
            });
        },
        
        /**
         * @private
         * @param {Event} ev
         */
        _onClickSend: function (ev) {
            ev.stopPropagation();
            ev.preventDefault();

            //VALIDACION DE DATOS: 
            var $primer_nombre = $('input[name="primer_nombre"]');
            var $segundo_nombre = $('input[name="segundo_nombre"]');
            var $email = $('input[name="email"]');
            var $phone = $('input[name="phone"]');
            var $tipo_documento = $("#tipo_documento option:selected");
            var $vat = $('input[name="vat"]');
            var $name = $('input[name="name"]');

            var $calle_billing = $('input[name="calle_billing"]');
            var $state_id = $("#state_id option:selected");
            var $city_id = $("#city_id option:selected");

            var $list_delivery = $("#list_delivery option:selected");
            var $calle_delivery = $('input[name="calle_delivery"]');
            var $state_id_delivery = $("#state_id_delivery option:selected");
            var $city_id_delivery = $("#city_id_delivery option:selected");

            var msg_alert = "";
            if (!$primer_nombre.val()){
                msg_alert += ">> Debe ingresar el campo [Nombres] \n";
            }

            if (!$segundo_nombre.val()){
                msg_alert += ">> Debe ingresar el campo [Apellidos] \n";
            }

            if (!$email.val()){
                msg_alert += ">> Debe ingresar el campo [Correo electrónico] \n";
            }

            if (!$phone.val()){
                msg_alert += ">> Debe ingresar el campo [Teléfono] \n";
            }else{
                if ($phone.val().length<7 || $phone.val().length>10){
                    msg_alert += ">> El número de teléfono/celular debe tener entre 7 y 10 números \n";
                }
            }

            if (!$vat.val()){
                msg_alert += ">> Debe ingresar el campo [Número de identidad] \n";
            }else{
                console.log("$tipo_documento.val()",$tipo_documento.val());
                console.log("$vat.val().length",$vat.val().length);
                if ($tipo_documento.val()=="C" && $vat.val().length!=10){
                    msg_alert += ">> Número de identidad incorrecto \n";
                }

                if ($tipo_documento.val()=="R" && $vat.val().length!=13){
                    msg_alert += ">> Número de identidad incorrecto \n";
                }
            }



            if (!$name.val()){
                msg_alert += ">> Debe ingresar el campo [Nombre completo/Razón social] \n";
            }

            if (!$calle_billing.val()){
                msg_alert += ">> Debe ingresar el campo [Calle, Número de Casa/Departamento y Referencia] \n";
            }

            if ($state_id.val()=="0"){
                msg_alert += ">> Debe ingresar el campo [Provincia] \n";
            }

            if ($city_id.val()=="0"){
                msg_alert += ">> Debe ingresar el campo [Ciudad] \n";
            }


            if ($list_delivery.val() != "1"){

                if (!$calle_delivery.val()){
                    msg_alert += ">> Debe ingresar el campo [Calle, Número de Casa/Departamento y Referencia] de la dirección de entrega\n";
                }

                if ($state_id_delivery.val()=="0"){
                    msg_alert += ">> Debe ingresar el campo [Provincia] de la dirección de entrega\n";
                }

                if ($city_id_delivery.val()=="0"){
                    msg_alert += ">> Debe ingresar el campo [Ciudad] de la dirección de entrega\n";
                }

            }
            
            


            var $row_items = $('#listitems_quote').children('tr');
            console.log("$row_items",$row_items);
            var item_list = [];
            var i=0;
            $("#listitems_quote tr").each(function() {
                if(i>0){
                    var json_list = {
                        "item" :$(this).data("item"),
                        "qty" :$(this).data("qty"),
                        "qty_id" :$(this).data("qty-id"),
                        "present_id" :$(this).data("present-id")
                    };
                    item_list.push(json_list);
                }
                i++;
            });

            if (item_list.length==0){
                msg_alert += ">> Debe agregar al menos un producto para cotizar \n";
            }

            if (msg_alert!=""){
                alert(msg_alert);
                return;
            }
            
            if (ev.type === 'submit') {
                var button = $('#btn-primary');
            } else {
                var button = ev.target;
            }
            
            if (!$(button).attr('disabled')){
                $(button).attr('disabled', true);
                $(button).children('.fa-lock').removeClass('fa-lock');
                $(button).prepend('<span class="o_loader"><i class="fa fa-refresh fa-spin"></i>&nbsp;</span>');
                console.log("desactiva boton");
            }else{
                return;
            }

            

            this._rpc({
                route: "/shop/quote/form_save",
                params: {
                    item_list: item_list,
                    'primer_nombre':$('input[name="primer_nombre"]').val(),
                    'segundo_nombre':$('input[name="segundo_nombre"]').val(),
                    'email':$('input[name="email"]').val(),
                    'phone':$('input[name="phone"]').val(),
                    'tipo_documento':$("#tipo_documento option:selected").val(),
                    'vat':$('input[name="vat"]').val(),
                    'name':$('input[name="name"]').val(),
                    'calle_billing':$('input[name="calle_billing"]').val(),
                    'state_id':$("#state_id option:selected").val(),
                    'city_id':$("#city_id option:selected").val(),
                    'list_delivery':$("#list_delivery option:selected").val(),
                    'calle_delivery':$('input[name="calle_delivery"]').val(),
                    'state_id_delivery':$("#state_id_delivery option:selected").val(),
                    'city_id_delivery':$("#city_id_delivery option:selected").val(),

                },
            }).then(function(data){
                console.log("data", data);
                
                $('.container_form_quote').addClass("d-none");
                $('p.o_iniciar_sesion').remove();
                
                var text = "";
                text += '<div class="s_alert_content">'
                text += '<p class="o_default_snippet_text">La cotización <strong>'+ data +'</strong> fue enviada a su correo<br/>'
                text += 'Puede dar seguimiento a sus cotizaciones desde la opción "Mi cuenta"'
                text += '</p></div>'
                $('#alert-save-form').append(text).removeClass("d-none");
                
                if ($(button).attr('disabled')){
                    $(button).attr('disabled', false);
                    $(button).children('.fa').addClass('fa-lock');
                    $(button).find('span.o_loader').remove();
                    console.log("activa boton");
                }
            });

           
        },
        /**
         * @private
         * @param {Event} ev
         */
        _onClickDeleteItem: function (ev) {
            console.log("Entro _onClickDeleteItem");
            var $input = $(ev.currentTarget);
            var line_id = $input.data("id");
            console.log("line_id",line_id);
            $('#line_item_'+(line_id).toString()).remove(); 
        },
        /**
         * @private
         * @param {Event} ev
         */
        _onChangeSelectProduct: function (ev) {
            console.log("Entro _onChangeSelectProduct");
            var $input = $(ev.currentTarget);
            var product_id = $input.val();
            console.log("product_id", product_id);
            if(product_id == "-1") 
                return;

            this._rpc({
                route: "/shop/quote/presentacion",
                params: {
                    product_id: product_id
                },
            }).then(function(data){
                console.log("data _onChangeSelectProduct", data);
                var list_opt = '<option class="form-control" style="color:black" value="-1">Seleccionar...</option>'; 
                for (var i = 0; i < data.length; i++) {
                    list_opt += '<option class="form-control" style="color:black" value="'+ data[i].id +'">' + data[i].name + '</option>';
                };

                $('#selectpresentacion').empty().append(list_opt);

                list_opt = '<option class="form-control" style="color:black" value="-1">Seleccionar...</option>'; 
                $('#selectcantidad').empty().append(list_opt);
            });
        }, 
        /**
         * @private
         * @param {Event} ev
         */
        _onChangeSelectPresentacion: function (ev) {
            console.log("Entro _onChangeSelectPresentacion");
            var $input = $(ev.currentTarget);
            var presentacion_id = $input.val();
            var product_id = $("#selectproduct").val();
            console.log("product_id", product_id);
            console.log("presentacion_id", presentacion_id);
            if(product_id == "-1") 
                return;

            if(presentacion_id == "-1") 
                return;

            this._rpc({
                route: "/shop/quote/cantidad",
                params: {
                    presentacion_id: presentacion_id,
                    product_id: product_id
                },
            }).then(function(data){
                console.log("data _onChangeSelectPresentacion", data);

                var list_opt = '<option class="form-control" style="color:black" value="-1">Seleccionar...</option>'; 
                for (var i = 0; i < data.length; i++) {
                    list_opt += '<option class="form-control" style="color:black" value="'+ data[i].id +'">' + data[i].name + '</option>';
                };

                
                $('#selectcantidad').empty().append(list_opt);
                
            });
        }, 
        /**
         * @private
         * @param {Event} ev
         */
         _onClickAddItem: function (ev) {
            console.log("Entro _onClickAddItem");

            //var $input = $(ev.currentTarget);
            var cantidad_id = $("#selectcantidad").children("option:selected");
            var $selectproduct = $("#selectproduct").children("option:selected");
            var $selectpresentacion = $("#selectpresentacion").children("option:selected");

            console.log("cantidad_id", cantidad_id);
            if(cantidad_id == "-1") 
                return;

            if($selectproduct.val() == "-1") 
                return;

            if($selectpresentacion.val() == "-1") 
                return;
            
            var $selectcantidad = $("#selectcantidad").children("option:selected");
            //var image_128 =  "/web/image/product.template/" + $selectproduct.val() + "/image_128/";
            var image_128 =  "/imagen_producto/" + $selectproduct.val() ;
            var product_name = $selectproduct.data("name");
            var cantidad = $selectcantidad.text();
            var presentacion = $selectpresentacion.text();
            var tr_text = "";
            
            var count = $('#listitems_quote').children('tr').length + 1;
            
            tr_text += '<tr id="line_item_' + count.toString() + '" data-item="'+$selectproduct.val()+'" data-qty="'+cantidad+'" data-present-id="'+$selectpresentacion.val()+'" data-qty-id="'+$selectcantidad.val()+'">';
            tr_text += '<td class="td-img text-center" colspan="2">';
            tr_text += '        <img src="' + image_128 + '" class="img rounded o_image_64_max" alt="' + product_name  + '">';
            tr_text += '    </td>';
            tr_text += '    <td class="td-product_name" colspan="6">';
            tr_text += '        <span>' + product_name + " - " + presentacion + '</span>';
            tr_text += '    </td>';
            tr_text += '    <td class="td-qty" colspan="2">';
            tr_text += '        <span>' + cantidad +'</span>';
            tr_text += '    </td>';
            tr_text += '    <td class="text-center td-delete" colspan="2">';
            tr_text += '        <a href="#" data-id="' + count.toString() +'" class="js_delete_item_quote" ><i class="fa fa-trash-o" ></i></a>';
            tr_text += '</td></tr>';

            $('#listitems_quote').append(tr_text);
        }       
    });


});