// Copyright (c) 2017, Lewin Villar and contributors
// For license information, please see license.txt

frappe.ui.form.on('Resultado', {
	onload: function(frm){
		setTimeout(function(){
			$("div[data-page-route='Form/Resultado'] .btn.btn-xs.btn-default.grid-add-row").hide();
		
			if(frm.doc.indices_urinarios)
			{
				$("div[data-fieldname='examen_fisicoquimico']").click(function(event){
			
					var indice =event.currentTarget.parentElement.childNodes[1].textContent;
					
					frappe.model.get_value("Indice Urinario",{"name":indice},"opciones",function(data){
				
						if(data)
						{
							frm.set_df_property("examen_fisicoquimico","options",data.opciones,frm.docname,"indices_urinarios");
							
							refresh_field("indices_urinarios");
						}	
					});
				});
				//remove eventsbefore adding it
				//$("[data-fieldname='sedimentos_urinarios'] [data-fieldname='sedimentos_urinarios'] div[data-fieldname='examen_fisicoquimico']").off("click");

				$("[data-fieldname='sedimentos_urinarios'] [data-fieldname='sedimentos_urinarios'] div[data-fieldname='examen_fisicoquimico']").click(function(event){
			
					var indice =event.currentTarget.parentElement.childNodes[1].textContent;
					
					frappe.model.get_value("Indice Urinario",{"name":indice},"opciones",function(data){
				
						if(data)
						{
							frm.set_df_property("examen_fisicoquimico","options",data.opciones,frm.docname,"sedimentos_urinarios");
							
							refresh_field("sedimentos_urinarios");
						}	
					});
				});
			}
		}, 500);		
	},
	refresh:function(frm){
		var tipoResultado = frm.doc.consulta_tipo=="Consulta Privada" ? "Consulta Prueba Privada":"Consulta Prueba" 
	
		frappe.model.get_value(tipoResultado,{"parent":frm.doc.consulta,"prueba":"PRB-000000195"},"name",function(data){
			if (data) {
				frappe.model.set_value(frm.doctype,frm.docname,"test_hematologico",1)	
			}
			else
			{
				frappe.model.set_value(frm.doctype,frm.docname,"test_hematologico",0)	
			}	
		});
		frappe.model.get_value(tipoResultado,{"parent":frm.doc.consulta,"prueba":"PRB-000000229"},"name",function(data){
			if (data) {
				frappe.model.set_value(frm.doctype,frm.docname,"test_urianalisis",1)	
			}
			else
			{
				frappe.model.set_value(frm.doctype,frm.docname,"test_urianalisis",0)	
			}	
		});

		cur_frm.set_query("consulta", function() {
				return {
					"filters": {"docstatus":1,"resultado":"0"}
				}
			});			

	},
	consulta_tipo: function(frm){
		
			cur_frm.set_query("consulta", function() {
				return {
					"filters": {"docstatus":1,"resultado":"0"}
				}
			});	

	},
	consulta: function(frm){
		
		if(frm.doc.consulta)
		{	
			
			frappe.call({"method": "frappe.client.get",
				args: {
					doctype: "Paciente",
					name: frm.doc.paciente
				},
				callback: function (data) {
					/*frappe.model.set_value(frm.doctype,frm.docname,"cedula",data.message.cedula_pasaporte?data.message.cedula_pasaporte:"-");
					frappe.model.set_value(frm.doctype,frm.docname,"sexo",data.message.sexo);
					frappe.model.set_value(frm.doctype,frm.docname,"edad",data.message.edad);
					frappe.model.set_value(frm.doctype,frm.docname,"direccion",data.message.direccion?data.message.direccion:"-");
					frappe.model.set_value(frm.doctype,frm.docname,"telefono",data.message.telefono?data.message.telefono:"-");
				*/}
				
			});
			
			$c("runserverobj",{"method": "get_list_indice_quimicos","docs":cur_frm.doc}, function(response){	
				refresh_many(["indices_pruebas", "indices_hematologicos", "indices_urinarios","recuento_diferencial","sedimentos_urinarios","serologia","sexo","edad","cedula_pasaporte","telefono","direccion"]);
			});
			frappe.dom.freeze("Espere...");
			
			//remove eventsbefore adding it
			//$("div[data-fieldname='examen_fisicoquimico']").off("click");
			
			setTimeout(function()
			{
				$("div[data-fieldname='examen_fisicoquimico']").click(function(event){
			
					var indice =event.currentTarget.parentElement.childNodes[1].textContent;
			
					
					
					frappe.model.get_value("Indice Urinario",{"name":indice},"opciones",function(data){
				
						if(data)
						{
							frm.set_df_property("examen_fisicoquimico","options",data.opciones,frm.docname,"indices_urinarios");
							
							refresh_field("indices_urinarios");
						}	
					});
					
				});
				//remove eventsbefore adding it
				//$("[data-fieldname='sedimentos_urinarios'] [data-fieldname='sedimentos_urinarios'] div[data-fieldname='examen_fisicoquimico']").off("click");

				$("[data-fieldname='sedimentos_urinarios'] [data-fieldname='sedimentos_urinarios'] div[data-fieldname='examen_fisicoquimico']").click(function(event){
			
					var indice =event.currentTarget.parentElement.childNodes[1].textContent;
					
					frappe.model.get_value("Indice Urinario",{"name":indice},"opciones",function(data){
				
						if(data)
						{
							frm.set_df_property("examen_fisicoquimico","options",data.opciones,frm.docname,"sedimentos_urinarios");
							
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
