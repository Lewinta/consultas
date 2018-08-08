// Copyright (c) 2016, Lewin Villar and contributors
// For license information, please see license.txt
frappe.ui.form.on('Consulta Privada', {
	onload: function(frm) {
		if (!frm.doc.__islocal) return;
		//frappe.model.set_value(frm.doctype, frm.docname, "fecha", new Date());
		var callback = function(data) {
			
			frappe.model.get_value("Empresa",data.empresa, "nombre", function (data){
				frappe.model.set_value(frm.doctype, frm.docname, "empresa", data.nombre);				
				console.log(data.nombre);
			});			
		};
		frappe.model.get_value("User", frappe.session.user, "empresa", callback);
	},
	medico: function(frm, cdt, cdn) {
		var tDiferencia = 0;
		var med=frm.doc.medico;
		if ( !frm.doc.medico) med="none";
		
		if (frm.doc.es_referido) {
			
			frm.doc.pruebas.forEach(function(child) {

				frappe.model.get_value("Lista Precio", {ars_medico: med,prueba: child.prueba}, "monto", function(data) {
					
					if (data) {
						
						child.diferencia=data.monto;
						refresh_field("pruebas");
					} 
					else {
						frappe.model.get_value("Prueba", child.prueba, "precio", function(dftl) {
					   
							child.diferencia=dftl.precio;
							refresh_field("pruebas");
						});
					}
					
				});
			});
		}
	},
	es_referido:function(frm, cdt, cdn) {
	   
		//Si el paciente es referido, debe existir algun medico
		if(frm.doc.es_referido)
			frm.set_df_property("medico","reqd",true);
		else
			frm.set_df_property("medico","reqd",false);

		var tDiferencia = 0;
		var med=frm.doc.medico;
		//if (!frm.doc.pruebas||!frm.doc.medico) return;
		if (!frm.doc.medico) med="none";
		if(frm.doc.pruebas)
		{	
			frm.doc.pruebas.forEach(function(child) {
				
				frappe.model.get_value("Lista Precio", {ars_medico: med,prueba: child.prueba}, "monto", function(data) {
					
					if (data && frm.doc.es_referido) {
						
						child.diferencia=data.monto;
						refresh_field("pruebas");
					} 
					else {
						frappe.model.get_value("Prueba", child.prueba, "precio", function(dftl) {
					   
							child.diferencia=dftl.precio;
							refresh_field("pruebas");
						});
					}
					
				});
			});
		}
	},
	validate: function(frm, cdt, cdn) {
		frappe.model.set_value(frm.doctype, frm.docname, "responsable", frappe.session.user);

		
		
	},
	before_submit:function(frm){
		
		var callback = function(data) {
		   // console.log(data);
			return;
		}

		if (frm.doc.es_referido) {
			frm.doc.pruebas.forEach(function(child) {

				frappe.model.get_value("Lista Precio", {
						prueba: child.prueba,
						ars_medico: frm.doc.medico
					},
					"monto",
					callback);
			});
			
			console.log("runserverobj");
			$c('runserverobj', {"method": "guardar_lista_de_precio", "docs": cur_frm.doc}, function(response){
				if(response.message){
					frappe.show_alert("Se ha agregado una Prueba nueva a la lista de Precio  " + frm.doc.medico,15);
				}
			});
		}
	}
});
frappe.ui.form.on("Consulta Prueba Privada", {
	prueba: function(frm, cdt, cdn) {
		var tDiferencia = 0;
		
		var row = locals[cdt][cdn];
		
		var busca_precio = function(data) {
			if (data && frm.doc.es_referido) //El precio esta en la lista de precios del medico o ARS
			{
				frappe.model.set_value(cdt, cdn, "diferencia", data.monto);
			} else //Tomamos el precio por defecto
			{
				frappe.model.get_value("Prueba", row.prueba, "precio", function(dftl) {
					frappe.model.set_value(cdt, cdn, "diferencia", dftl.precio);
				});
			}
			frm.doc.pruebas.forEach(function(child) {
				tDiferencia += child.diferencia;
				frappe.model.set_value(frm.doctype, frm.docname, "diferencia", tDiferencia);
			});
		}
		var med=frm.doc.medico;
		if (!frm.doc.medico) med="none";
		
		if (row.prueba) frappe.model.get_value("Lista Precio", {ars_medico: med,prueba: row.prueba},"monto", busca_precio);
		else frm.get_field("pruebas").grid.grid_rows[row.idx-1].remove();
	},
	diferencia: function(frm, cdt, cdn) {
		var tDiferencia = 0;
		var row = locals[cdt][cdn];

		frm.doc.pruebas.forEach(function(child) {
			tDiferencia += child.diferencia;
			frappe.model.set_value(frm.doctype, frm.docname, "diferencia", tDiferencia);

		});
	},
	pruebas_remove: function(frm,cdt,cdn) {
		var tDiferencia = 0;
		var row = locals[cdt][cdn];

		if(frm.doc.pruebas.length > 0){
			frm.doc.pruebas.forEach(function(child) {
			tDiferencia += eval(child.diferencia);
			frappe.model.set_value(frm.doctype, frm.docname, "diferencia", tDiferencia);

			});
		}else{
			frappe.model.set_value(frm.doctype, frm.docname, "diferencia", 0);
		}
	}

});