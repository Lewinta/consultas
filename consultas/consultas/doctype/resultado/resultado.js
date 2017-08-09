// Copyright (c) 2017, Lewin Villar and contributors
// For license information, please see license.txt
frappe.ui.form.on('Resultado', {

    onload_post_render: function(frm) {
        /*var microbiologia_sb = $('.section-head').find("a").filter(function(){ return $(this).text() == "Microbiologia" ;}).parent()
        var fields = ["titulo","antibiogramas" ]
        var current_table
        

        fields.forEach(function(indice){
			frm.set_df_property(indice,"hidden",1);
        })
		microbiologia_sb.on("click", function(){
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
        */setTimeout(function() {
            //$("div[data-page-route='Form/Resultado'] .btn.btn-xs.btn-default.grid-add-row").hide();
            set_events(frm)
            //}
        }, 1000);
    },
    refresh: function(frm) {
        refresh_modules(frm);

        if(frm.doc.docstatus == 0)
            frm.trigger("add_toolbar_buttons")

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
   eventos: function(frm){
    setTimeout(function() {
            //$("div[data-page-route='Form/Resultado'] .btn.btn-xs.btn-default.grid-add-row").hide();
            set_events(frm)
            //}
        }, 300);

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
                "method": "get_table_items",
                "docs": frm.doc
            }, function(response) {
                refresh_many([
                	"indices_pruebas", 
                	"indices_hematologicos", 
                	"indices_urinarios", 
                	"recuento_diferencial", 
                	"sedimentos_urinarios", 
                	"serologia", 
                	"sexo", 
                	"edad", 
                	"cedula_pasaporte", 
                	"telefono", 
                	"direccion",
                	"antibiogramas",
                	"inmunodiagnosticos",
                    "tipificacion",
                    "hormonas",
                    "aspecto_fisico",
                    "aspecto_microscopico",
                    "nombre_completo"
                    ]);
                frm.refresh();
            });
            frappe.dom.freeze("Espere...");
            //remove eventsbefore adding it
            //$("div[data-fieldname='examen_fisicoquimico']").off("click");
            setTimeout(function() {
              set_events(frm)

              /*  $("div[data-fieldname='examen_fisicoquimico']").click(function(event) {
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
                });*/
            }, 2000);
            //setTimeout(function(){frappe.dom.unfreeze();},2000);
        }
        frappe.dom.unfreeze();
    },
    add_toolbar_buttons: function(frm){
        
        var personal_info = function(){
            $c('runserverobj', {"method": "refresh_personal_info", "docs": frm.doc}, function(response){
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

            });
        }

        var hematologia = function(){
            $c('runserverobj', {"method": "get_hematologia", "docs": frm.doc}, function(response){
                if(response.message){
                    refresh_field("indices_hematologicos")
                    refresh_field("otros_hematologia")
                    frappe.show_alert("Hematologia Actualizado!",5);
                }

            });
        }

        var quimica = function(){
            $c('runserverobj', {"method": "get_quimica", "docs": frm.doc}, function(response){
                if(response.message){
                    refresh_field("indices_pruebas")
                    frappe.show_alert("Quimica Actualizada!",5);
                }

            });
        }

        var serologia = function(){
            $c('runserverobj', {"method": "get_serologia", "docs": frm.doc}, function(response){
                if(response.message){
                    refresh_field("serologia")
                    frappe.show_alert("Serologia Actualizada!",5);
                }

            });
        }

        var inmunodiagnosticos = function(){
            $c('runserverobj', {"method": "get_inmunodiagnostico", "docs": frm.doc}, function(response){
                if(response.message){
                    refresh_field("inmunodiagnosticos")
                    frappe.show_alert("Inmunodiagnosticos Actualizados!",5);
                }

            });
        }

        var hormonas = function(){
            $c('runserverobj', {"method": "get_hormonas", "docs": frm.doc}, function(response){
                if(response.message){
                    refresh_field("hormonas")
                    frappe.show_alert("Hormonas Actualizadas!",5);
                }

            });
        }

        var tipificacion = function(){
            $c('runserverobj', {"method": "get_tipificacion", "docs": frm.doc}, function(response){
                if(response.message){
                    refresh_field("tipificacion")
                    frappe.show_alert("Tipificacion Actualizada!",5);
                }

            });
        }

        var urianalisis = function(){
            $c('runserverobj', {"method": "get_urianalisis", "docs": frm.doc}, function(response){
                if(response.message){
                    refresh_field("indices_urinarios")
                    refresh_field("sedimentos_urinarios")
                    set_events()
                    frappe.show_alert("Urianalisis Actualizado!",5);
                }

            });
        }

        var coprologia = function(){
            $c('runserverobj', {"method": "get_coprologia", "docs": frm.doc}, function(response){
                if(response.message){
                    refresh_field("aspecto_fisico")
                    refresh_field("aspecto_microscopico")
                    set_events()
                    frappe.show_alert("Coprologia Actualizada!",5);
                }

            });
        }

        var anexos = function(){
            $c('runserverobj', {"method": "get_anexos", "docs": frm.doc}, function(response){
                if(response.message){
                    refresh_anexos(frm)
                    frappe.show_alert("Anexos Actualizado!",5);
                }

            });
        }

        frm.add_custom_button("Informacion Personal",personal_info,"Actualizar" )
        frm.add_custom_button("Hematologia",hematologia,"Actualizar" )
        frm.add_custom_button("Quimica",quimica,"Actualizar" )
        frm.add_custom_button("Serologia",serologia,"Actualizar" )
        frm.add_custom_button("Inmunodiagnosticos",inmunodiagnosticos,"Actualizar" )
        frm.add_custom_button("Hormonas",hormonas,"Actualizar" )
        frm.add_custom_button("Tipificacion",tipificacion,"Actualizar" )
        frm.add_custom_button("Urianalisis",urianalisis,"Actualizar" )
        frm.add_custom_button("Coprologia",coprologia,"Actualizar" )
        frm.add_custom_button("Anexos",anexos,"Actualizar" )
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
    frappe.model.get_value(tipoResultado, {"parent": frm.doc.consulta,"prueba": "PRB-000000229"}, "prueba_nombre", function(data) {
        if (data) {
            frm.set_value("test_urianalisis", 1)
        } 
        else {
            frm.set_value("test_urianalisis", 0)
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
function set_events(frm)
{
    console.log("events added")
    $("div[data-fieldtype='Table']").mouseenter(function(event){
        
        current_table = event.currentTarget.dataset.fieldname
    })

           // if (frm.doc.indices_urinarios) {
    $("div[data-fieldname='examen_fisicoquimico']").click(function(event) {
        var indice = event.currentTarget.parentElement.childNodes[1].textContent;
        frappe.model.get_value("Indice Urinario", {
            "name": indice
        }, "opciones", function(data) {
            if (data) {
                frm.set_df_property("examen_fisicoquimico", "options", data.opciones, frm.docname, current_table);
                refresh_field(current_table);
                
            }
        });
    });
                //remove eventsbefore adding it
                //$("[data-fieldname='sedimentos_urinarios'] [data-fieldname='sedimentos_urinarios'] div[data-fieldname='examen_fisicoquimico']").off("click");
        $("[data-fieldname='sedimentos_urinarios'] [data-fieldname='sedimentos_urinarios'] div[data-fieldname='examen_fisicoquimico']").click(function(event) {
            var indice = event.currentTarget.parentElement.childNodes[1].textContent;
            frappe.model.get_value("Indice Urinario", {
                "name": indice,
                "coprologico":0
            }, "opciones", function(data) {
                if (data) {
                    frm.set_df_property("examen_fisicoquimico", "options", data.opciones, frm.docname, "sedimentos_urinarios");
                    refresh_field("sedimentos_urinarios");
                }
            });
        });
}