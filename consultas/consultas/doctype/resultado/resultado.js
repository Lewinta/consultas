// Copyright (c) 2017, Lewin Villar and contributors
// For license information, please see license.txt
frappe.ui.form.on('Resultado', {

    onload_post_render: function(frm) {
        frm.trigger('eventos')
        var microbiologia_section = $('.section-head').find("a").filter(function(){ return $(this).text() == "Microbiologia" ;}).parent()
        var antibiograma_section = $('.section-head').find("a").filter(function(){ return $(this).text() == "Antibiogramas" ;}).parent()
        
        microbiologia_section.on("click", function(){
            if ($(this).hasClass("collapsed")){
                antibiograma_section.collapse()
            }
            else{
                antibiograma_section.collapse()
            }

        })

        frm.add_fetch("consulta", "paciente", "paciente")
        frm.add_fetch("consulta", "edad", "edad")
        frm.add_fetch("consulta", "sucursal", "sucursal")
    },
    validate: function (frm){
        frm.set_value("hematologia_chequeados", 0);
       $.map(frm.doc.indices_hematologicos, (row)=>{
            var res = eval_result(row.rango_referencia, row.resultado);
            var cdt = row.doctype;
            var cdn = row.name;
            if (res){
                console.log(res);
                console.log(row);
                frappe.model.set_value(cdt, cdn, "resultado", res);
            }
            if (row.resultado && typeof(row.resultado) == "string" && row.resultado.includes("*"))
                frm.set_value("hematologia_chequeados", 1);
                
       });
       $.map(frm.doc.recuento_diferencial, (row)=>{
            var res = eval_result(row.rango_referencia, row.resultado);
            var cdt = row.doctype;
            var cdn = row.name;
            if (res){
                console.log(res);
                console.log(row);
                frappe.model.set_value(cdt, cdn, "resultado", res);
            }
            if (row.resultado && typeof(row.resultado) == "string" && row.resultado.includes("*"))
                frm.set_value("hematologia_chequeados", 1);


       });
        
        frm.set_value("quimica_chequeados", 0);
       $.map(frm.doc.indices_pruebas, (row)=>{
            var res = eval_result(row.rango_ref, row.resultado);
            var cdt = row.doctype;
            var cdn = row.name;
            if (res){
                console.log(res);
                console.log(row);
                frappe.model.set_value(cdt, cdn, "resultado", res);
            }
            if (row.resultado && typeof(row.resultado) == "string" && row.resultado.includes("*"))
                frm.set_value("quimica_chequeados", 1);
       });
    },
    organismo: function(frm) {
        frm.set_value("organismo", frm.doc.organismo.toUpperCase())
    },
    refresh: function(frm) {
        //refresh_modules(frm);
        frm.add_fetch("consulta", "medico", "medico");
        frm.add_fetch("consulta", "institucion", "institucion")
        if(frm.doc.docstatus == 0)
            frm.trigger("add_toolbar_buttons")

        frm.trigger("consulta_tipo")
    },
    consulta_tipo: function(frm) {
        cur_frm.set_query("consulta", function() {
            return {
                "filters": {
                    // "docstatus": 1,
                    "resultado": ""
                }
            }
        });
    },
   eventos: function(frm){
    setTimeout(function() {
            //$("div[data-page-route='Form/Resultado'] .btn.btn-xs.btn-default.grid-add-row").hide();
            set_events(frm)
            //}
        }, 1000);

   },
   tiene_parasitos: function(frm){
    frm.set_value("parasitos", frm.doc.tiene_parasitos ? "":"NO SE OBSERVAN ELEMENTOS PARASITARIOS EN ESTA MUESTRA.")

   },
   tiene_amebas: function(frm){
    frm.set_value("amebas", frm.doc.tiene_amebas ? "":"NO SE OBSERVAN EN ESTA MUESTRA.")

   },
   tiene_giardia: function(frm){
    frm.set_value("giardia", frm.doc.tiene_giardia ? "":"NO SE OBSERVAN EN ESTA MUESTRA.")

   },
   parasitos: function(frm){
    frm.set_value("parasitos", frm.doc.parasitos.toUpperCase())
   },
   amebas: function(frm){
    frm.set_value("amebas", frm.doc.amebas.toUpperCase())
   },
   giardia: function(frm){
    frm.set_value("giardia", frm.doc.giardia.toUpperCase())
   },
   tiene_parasitos_heces: function(frm){
    frm.set_value("parasitos_heces", frm.doc.tiene_parasitos_heces ? "":"NO SE OBSERVAN ELEMENTOS PARASITARIOS EN ESTA MUESTRA.")
   },
   tiene_amebas_heces: function(frm){
    frm.set_value("amebas_heces", frm.doc.tiene_amebas_heces ? "":"NO SE OBSERVAN EN ESTA MUESTRA.")
   },
   tiene_giardia_heces: function(frm){
    frm.set_value("giardia_heces", frm.doc.tiene_giardia_heces ? "":"NO SE OBSERVAN EN ESTA MUESTRA.")
   },
   parasitos_heces: function(frm){
    frm.set_value("parasitos_heces", frm.doc.parasitos_heces.toUpperCase())
   },
   amebas_heces: function(frm){
    frm.set_value("amebas_heces", frm.doc.amebas_heces.toUpperCase())
   },
   giardia_heces: function(frm){
    frm.set_value("giardia_heces", frm.doc.giardia_heces.toUpperCase())
   },
    paciente: function(frm) {
        if (frm.doc.consulta) {
            let fields = ["cedula_pasaporte", "sexo", "edad", "telefono"]
            frappe.db.get_value("Paciente", frm.doc.paciente, fields)
                .done((data) => $.each(data.message, (key, value) => frm.set_value(key, value || "-")));

            var _method = "get_table_items"
            var _args = "get_table_items"

            frappe.call({
            	"method":"get_table_items",
            	"doc":frm.doc,
            	callback: function(response){
            		if(response){

            			frappe.run_serially([
            		    	frm.refresh(),
            		    	frappe.dom.freeze("Espere..."),
            		    	set_events(frm),
            		    	frappe.dom.unfreeze()
            			]);
            		}
            	}
            });
        }
    },
    add_toolbar_buttons: function(frm){
        
        var personal_info = function(){
            frappe.call({"method": "refresh_personal_info", "doc": frm.doc,
            	callback:function(response){
	                if(response.message){
	                    frappe.show_alert("Cliente Actualizado!",5);
	                    refresh_field("cedula_pasaporte")
	                    refresh_field("sexo")
	                    refresh_field("edad")
	                    refresh_field("telefono")
	                    refresh_field("direccion")
	                    refresh_field("medico")
	                    refresh_field("nombre_completo")
	                    frm.dirty()
	                }

	            }
        	});
        }

        var hematologia = function(){
            frappe.call({"method": "get_hematologia", "doc": frm.doc, callback:function(response){
                if(response.message){
                    frm.refresh();
                    frappe.show_alert("Hematologia Actualizado!",5);
                    frm.dirty()
                }

            }});
        }

        var quimica = function(){
            frappe.call({"method": "get_quimica", "doc": frm.doc, callback:function(response){
                if(response.message){
                    refresh_field("indices_pruebas")
                    frm.refresh_fields("test_quimicos")
                    frappe.show_alert("Quimica Actualizada!",5);
                    frm.dirty()
                }

            }});
        }

        var microbiologia = function(){
            frappe.call({"method": "get_microbiologia", "doc": frm.doc, callback:function(response){
                if(response.message){
                    refresh_field("antibiogramas")
                    frm.refresh_fields("test_microbiologia")
                    frappe.show_alert("Microbiologia Actualizada!",5);
                    frm.dirty()
                }

            }});
        }

        var serologia = function(){
            frappe.call({"method": "get_serologia", "doc": frm.doc, callback:function(response){
                if(response.message){
                    refresh_field("serologia")
                    frappe.show_alert("Serologia Actualizada!",5);
                    frm.dirty()
                }

            }});
        }

        var inmunodiagnosticos = function(){
            frappe.call({"method": "get_inmunodiagnostico", "doc": frm.doc, callback:function(response){
            
                frappe.run_serially([
                    frappe.dom.freeze(),
                    frm.refresh(),
                    response && response.message && console.log("Inmunodiagnosticos"),
                    frappe.dom.unfreeze()
                ]); 
                frappe.show_alert("Inmunodiagnosticos Actualizados!",5);
                frm.dirty()

            }});
        }

        var hormonas = function(){
            frappe.call({"method": "get_hormonas", "doc": frm.doc, callback:function(response){
                if(response.message){
                    frappe.show_alert("Hormonas Actualizadas!",5);
                    frm.refresh();
                    frm.dirty()
                }

            }});
        }

        var tipificacion = function(){
            frappe.call({"method": "get_tipificacion", "doc": frm.doc, callback:function(response){
                if(response.message){
                    frappe.show_alert("Tipificacion Actualizada!",5);
                    frm.refresh();
                    frm.dirty()
                }

            }});
        }

        var urianalisis = function(){
            frappe.call({"method": "get_urianalisis", "doc": frm.doc, callback:function(response){
                if(response.message){
                    refresh_field("indices_urinarios")
                    refresh_field("sedimentos_urinarios")
                    set_events()
                    frm.refresh()
                    frappe.show_alert("Urianalisis Actualizado!",5);
                    frm.dirty()
                }

            }});
        }

        var otros_urianalisis = function(){
            frappe.call({"method": "get_otros_uroanalisis", "doc": frm.doc, callback:function(response){
                if(response.message){
                    refresh_field("otros_uroanalisis")
                    set_events()
                    frm.refresh()
                    frappe.show_alert("Otros Uroanalisis Actualizado!",5);
                    frm.dirty()
                }

            }});
        }

        var coprologia = function(){
            frappe.call({"method": "get_coprologia", "doc": frm.doc, callback:function(response){
                if(response.message){
                    frm.refresh()
                    frm.dirty()
                    set_events()
                    frappe.show_alert("Coprologia Actualizada!",5);
                    frm.dirty()
                }

            }});
        }

        var anexos = function(){
            frappe.call({"method": "get_anexos", "doc": frm.doc, callback:function(response){
                if(response.message){
                    frm.refresh()
                    refresh_anexos(frm)
                    frappe.show_alert("Anexos Actualizado!",5);
                    frm.dirty()
                }

            }});
        }

        var espermatograma = function(){
            frappe.call({"method": "get_espermatograma", "doc": frm.doc, callback:function(response){
                if(response.message){
                    frm.refresh()
                    frm.refresh_fields("test_espermatograma")
                    frm.refresh_fields("examen_macroscopico")
                    frm.dirty()
                    frappe.show_alert("Espermatograma Actualizado!",5);
                    frm.dirty()
                }

            }});
        }

        var especiales = function(){
            frappe.call({"method": "get_especiales", "doc": frm.doc, callback:function(response){
                if(response.message){
                    frm.refresh()
                    frm.refresh_fields("test_especiales")
                    frm.dirty()
                    frappe.show_alert("Especiales Actualizado!",5);
                    frm.dirty()
                }
            
            }});
        }

        frm.add_custom_button("Informacion Personal",personal_info,"Actualizar" )
        frm.add_custom_button("Hematologia",hematologia,"Actualizar" )
        frm.add_custom_button("Microbiologia",microbiologia,"Actualizar" )
        frm.add_custom_button("Quimica",quimica,"Actualizar" )
        frm.add_custom_button("Serologia",serologia,"Actualizar" )
        frm.add_custom_button("Inmunodiagnosticos",inmunodiagnosticos,"Actualizar" )
        frm.add_custom_button("Hormonas",hormonas,"Actualizar" )
        frm.add_custom_button("Tipificacion",tipificacion,"Actualizar" )
        frm.add_custom_button("Otros Urianalisis",otros_urianalisis,"Actualizar" )
        frm.add_custom_button("Urianalisis",urianalisis,"Actualizar" )
        frm.add_custom_button("Coprologia",coprologia,"Actualizar" )
        frm.add_custom_button("Espermatograma",espermatograma,"Actualizar" )
        frm.add_custom_button("Anexos",anexos,"Actualizar" )
        frm.add_custom_button("Especiales",especiales,"Actualizar" )
    }
});
frappe.ui.form.on("Resultado Quimica", {
    resultado:(frm, cdt, cdn) =>{
        let row = frappe.model.get_doc(cdt, cdn);
        let result = eval_result(row.rango_ref, row.resultado);
        if (result)
            frappe.model.set_value(cdt, cdn, "resultado", result);

        frm.refresh_field("indices_pruebas");
    }

});
frappe.ui.form.on("Resultados Hematologicos", {
    resultado:(frm, cdt, cdn) =>{
        let row = frappe.model.get_doc(cdt, cdn);
        let result = eval_result(row.rango_referencia, row.resultado);
        if (result)
            frappe.model.set_value(cdt, cdn, "resultado", result);

        frm.refresh_field("indices_pruebas");
    }

});

function refresh_anexos(frm){

	refresh_field("test_prb_000000065")
	refresh_field("tsh_heading")
	refresh_field("prb_000000065")
	refresh_field("test_prb_000000177")
	refresh_field("fsh_heading")
	refresh_field("prb_000000177")
	refresh_field("bhcg_heading")
	refresh_field("prb_000000120")
	refresh_field("test_prb_000000065")
}

function refresh_modules(frm) {

    var tipoResultado = frm.doc.consulta_tipo == "Consulta Privada" ? "Consulta Prueba Privada" : "Consulta Prueba";

    /*frappe.model.get_value(tipoResultado, {"parent": frm.doc.consulta,"prueba": "PRB-000000195"}, "prueba_nombre", function(data) {
        if (data) {
            frm.set_value("test_hematologico", 1)
        } 
        else {
            frm.set_value("test_hematologico", 0)
        }
    });*/
    
    frappe.model.get_value(tipoResultado, {"parent": frm.doc.consulta,"prueba": "PRB-000000144"}, "prueba_nombre", function(data) {
        if (data) {
            frm.set_value("test_coprologico", 1)
        } 
        else {
            frm.set_value("test_coprologico", 0)
        }
    }); 
    frappe.model.get_value(tipoResultado, {"parent": frm.doc.consulta,"prueba": "PRB-000000194"}, "prueba_nombre", function(data) {
        if (data) {
            frm.set_value("test_microbiologia", 1)
        } 
        else {
            frm.set_value("test_microbiologia", 0)
        }
    });
    frappe.model.get_value(tipoResultado, {"parent": frm.doc.consulta,"prueba": "PRB-000000191"}, "prueba_nombre", function(data) {
        if (data) {
            frm.set_value("test_microbiologia", 1)
        } 
        else {
            frm.set_value("test_microbiologia", 0)
        }
    });
   
   /* frappe.model.get_value(tipoResultado, {"parent": frm.doc.consulta,"prueba": "PRB-000000224"}, "prueba_nombre", function(data) {
        if (data) {
            frm.set_value("test_inmunodiagnosticos", 1)
        } 
        else {
            frm.set_value("test_inmunodiagnosticos", 0)
        }
    });*/
    /*frappe.model.get_value(tipoResultado, {"parent": frm.doc.consulta,"prueba": "PRB-000000224"}, "prueba_nombre", function(data) {
        if (data) {
            
            frm.set_value("test_tipificacion", 1)
        } 
        else {
            frm.set_value("test_tipificacion", 0)
        }
    });*/
}
function eval_result(eval_range, result){

    var eval_range = clean_str(eval_range);
    var result = clean_str(result);


    if (eval_range.includes("-")){
        // This is a range let's get min and max
        var min = eval_range.split("-")[0];
        var max = eval_range.split("-")[1];
        
        // console.log("min: " + min + " max: "+ max +" result: "+ result);

        if (isNaN(result) || isNaN(min) || isNaN(max))
        {
            // console.log("Alguno de los datos no es un numero");
            // If is not a number then i can't do nothing with it 
            return result
        }

        min = eval(min);
        max = eval(max);
        result = roundNumber(result, 3);

        if (result < min || result > max)
        {
            // The result is out of range, * was added
            // console.log("Out of range, * added");
            
            return result+"*"
        }

        return result
    }
    else if (eval_range.includes("&lt;=") || eval_range.includes("<=")){

        // console.log("result:"+result+" > range:"+eval_range);

        if (isNaN(result))
            return result
        
        eval_range = eval_range.replace("&lt;=", "");
        eval_range = eval_range.replace("<=", "");
        result = roundNumber(result, 3);
        if (result > eval(eval_range)){
            // console.log("Out of range, * added");
            return result+"*" 
        }

        return result
    }
    // else if (eval_range.includes("<")){
    else if (eval_range.includes("&lt;") || eval_range.includes("<") ){

        // console.log("result:"+result+" >= range:"+eval_range);

        if (isNaN(result))
            return result
        
        eval_range = eval_range.replace("&lt;", "");
        eval_range = eval_range.replace("<", "");
        result = roundNumber(result, 3);
        

        if (result >= eval(eval_range)){
            // console.log("Out of range, * added");
            return result+"*" 
        }

        return result
    }
    else if (eval_range.includes("&gt;=") || eval_range.includes(">=")){

        // console.log("result:"+result+" < range:"+eval_range);

        if (isNaN(result))
            return result
        
        eval_range = eval_range.replace("&gt;=", "");
        eval_range = eval_range.replace(">=", "");
        result = roundNumber(result, 3);
        if (result < eval(eval_range)){
            // console.log("Out of range, * added");
            return result+"*"
        } 

        return result
    }
    else if (eval_range.includes(">") || eval_range.includes("&gt;")){

        // console.log("result:"+result+" <= range:"+eval_range);

        if (isNaN(result))
            return result
        
        eval_range = eval_range.replace("&gt;", "");
        eval_range = eval_range.replace(">", "");
        result = roundNumber(result, 3);
        if (result <= eval(eval_range)){
            // console.log("Out of range, * added");
            return result+"*"
        } 

        return result
    }

    return result
}

function clean_str(s) {
    if (!s || typeof(s) == "number")
        return 
    // console.log("Cleaning s: "+s);

    let temp = s
    
    // Let's remove double dots
    temp = s ? s.replace("..",".") : temp ;
    // console.log("Cleaning temp: "+temp);

    // Let's remove spaces
    temp = replace_all(temp, " ","");
    
    // Let's asterix
    temp = replace_all(temp, "*","");

    // console.log("Return temp: "+temp);

    return temp
}

function set_events(frm)
{
    
    $("div[data-fieldtype='Table']").mouseenter(function(event){
        
        current_table = event.currentTarget.dataset.fieldname
    })

    $("div[data-fieldname='examen_fisicoquimico']").click(function(event) {
        var indice = event.currentTarget.parentElement.childNodes[1].textContent;
        frappe.model.get_value("Indice Urinario", {
            "name": indice
        }, "opciones", function(data) {
            if (data) {
                cur_frm.set_df_property("examen_fisicoquimico", "options", data.opciones, cur_frm.docname, current_table);
                refresh_field(current_table);
                
            }
        });
    });
    $("[data-fieldname='sedimentos_urinarios'] [data-fieldname='sedimentos_urinarios'] div[data-fieldname='examen_fisicoquimico']").click(function(event) {
        var indice = event.currentTarget.parentElement.childNodes[1].textContent;
        frappe.model.get_value("Indice Urinario", {
            "name": indice,
            "coprologico":0
        }, "opciones", function(data) {
            if (data) {
                cur_frm.set_df_property("examen_fisicoquimico", "options", data.opciones, cur_frm.docname, "sedimentos_urinarios");
                refresh_field("sedimentos_urinarios");
            }
        });
    });
    console.log("events added")
}
