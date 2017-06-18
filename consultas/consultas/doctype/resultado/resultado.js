// Copyright (c) 2017, Lewin Villar and contributors
// For license information, please see license.txt
frappe.ui.form.on('Resultado', {

    onload_post_render: function(frm) {
    	var section_head = $('.section-head').find("a").filter(function(){ return $(this).text() == "Microbiologia" ;}).parent()
        frm.set_df_property("titulo","hidden",1);
		frm.set_df_property("antibiogramas","hidden",1);
		console.log("section head", section_head)
		section_head.on("click", function(){
			if(!$(this).hasClass("collapsed"))
			{
                frm.set_df_property("antibiogramas","hidden",0);
				frm.set_df_property("titulo","hidden",0);
			}
			else
			{
                frm.set_df_property("titulo","hidden",1);
				frm.set_df_property("antibiogramas","hidden",1);
			}	
		});
        setTimeout(function() {
            //$("div[data-page-route='Form/Resultado'] .btn.btn-xs.btn-default.grid-add-row").hide();
            if (frm.doc.indices_urinarios) {
                $("div[data-fieldname='examen_fisicoquimico']").click(function(event) {
                    var indice = event.currentTarget.parentElement.childNodes[1].textContent;
                    frappe.model.get_value("Indice Urinario", {
                        "name": indice
                    }, "opciones", function(data) {
                        if (data) {
                            frm.set_df_property("examen_fisicoquimico", "options", data.opciones, frm.docname, "indices_urinarios");
                            refresh_field("indices_urinarios");
                        }
                    });
                });
                //remove eventsbefore adding it
                //$("[data-fieldname='sedimentos_urinarios'] [data-fieldname='sedimentos_urinarios'] div[data-fieldname='examen_fisicoquimico']").off("click");
                $("[data-fieldname='sedimentos_urinarios'] [data-fieldname='sedimentos_urinarios'] div[data-fieldname='examen_fisicoquimico']").click(function(event) {
                    var indice = event.currentTarget.parentElement.childNodes[1].textContent;
                    frappe.model.get_value("Indice Urinario", {
                        "name": indice
                    }, "opciones", function(data) {
                        if (data) {
                            frm.set_df_property("examen_fisicoquimico", "options", data.opciones, frm.docname, "sedimentos_urinarios");
                            refresh_field("sedimentos_urinarios");
                        }
                    });
                });
            }
        }, 500);
    },
    refresh: function(frm) {
        refresh_modules(frm);
        cur_frm.set_query("consulta", function() {
            return {
                "filters": {
                    "docstatus": 1,
                    "resultado": "0"
                }
            }
        });
    },
    consulta_tipo: function(frm) {
        cur_frm.set_query("consulta", function() {
            return {
                "filters": {
                    "docstatus": 1,
                    "resultado": "0"
                }
            }
        });
    },
    consulta: function(frm) {
        
        refresh_modules(frm);		
        if (frm.doc.consulta) {
            frappe.call({
                "method": "frappe.client.get",
                args: {
                    doctype: "Paciente",
                    name: frm.doc.paciente
                },
                callback: function(data) {
                    frappe.model.set_value(frm.doctype,frm.docname,"cedula_pasaporte",data.message.cedula_pasaporte?data.message.cedula_pasaporte:"-");
					frappe.model.set_value(frm.doctype,frm.docname,"sexo",data.message.sexo);
					frappe.model.set_value(frm.doctype,frm.docname,"edad",data.message.edad);
					frappe.model.set_value(frm.doctype,frm.docname,"direccion",data.message.direccion?data.message.direccion:"-");
					frappe.model.set_value(frm.doctype,frm.docname,"telefono",data.message.telefono?data.message.telefono:"-");
			   }
            });
            $c("runserverobj", {
                "method": "get_list_indice_quimicos",
                "docs": frm.doc
            }, function(response) {
                refresh_many(["indices_pruebas", "indices_hematologicos", "indices_urinarios", "recuento_diferencial", "sedimentos_urinarios", "serologia", "sexo", "edad", "cedula_pasaporte", "telefono", "direccion","antibiogramas"]);
            });
            frappe.dom.freeze("Espere...");
            //remove eventsbefore adding it
            //$("div[data-fieldname='examen_fisicoquimico']").off("click");
            setTimeout(function() {
                $("div[data-fieldname='examen_fisicoquimico']").click(function(event) {
                    var indice = event.currentTarget.parentElement.childNodes[1].textContent;
                    frappe.model.get_value("Indice Urinario", {
                        "name": indice
                    }, "opciones", function(data) {
                        if (data) {
                            frm.set_df_property("examen_fisicoquimico", "options", data.opciones, frm.docname, "indices_urinarios");
                            refresh_field("indices_urinarios");
                        }
                    });
                });
                //remove eventsbefore adding it
                //$("[data-fieldname='sedimentos_urinarios'] [data-fieldname='sedimentos_urinarios'] div[data-fieldname='examen_fisicoquimico']").off("click");
                $("[data-fieldname='sedimentos_urinarios'] [data-fieldname='sedimentos_urinarios'] div[data-fieldname='examen_fisicoquimico']").click(function(event) {
                    var indice = event.currentTarget.parentElement.childNodes[1].textContent;
                    frappe.model.get_value("Indice Urinario", {
                        "name": indice
                    }, "opciones", function(data) {
                        if (data) {
                            frm.set_df_property("examen_fisicoquimico", "options", data.opciones, frm.docname, "sedimentos_urinarios");
                            refresh_field("sedimentos_urinarios");
                        }
                    });
                });
            }, 3000);
            //setTimeout(function(){frappe.dom.unfreeze();},2000);
        }
        frappe.dom.unfreeze();
    }
});

function refresh_modules(frm) {

    var tipoResultado = frm.doc.consulta_tipo == "Consulta Privada" ? "Consulta Prueba Privada" : "Consulta Prueba";

    frappe.model.get_value(tipoResultado, {"parent": frm.doc.consulta,"prueba": "PRB-000000195"}, "prueba_nombre", function(data) {
        if (data) {
            frm.set_value("test_hematologico", 1)
        } 
        else {
            frm.set_value("test_hematologico", 0)
        }
    });
    frappe.model.get_value(tipoResultado, {"parent": frm.doc.consulta,"prueba": "PRB-000000229"}, "prueba_nombre", function(data) {
        if (data) {
            frm.set_value("test_urianalisis", 1)
        } 
        else {
            frm.set_value("test_urianalisis", 0)
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
}