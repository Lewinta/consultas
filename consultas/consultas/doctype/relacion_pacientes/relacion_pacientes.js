// Copyright (c) 2017, Lewin Villar and contributors
// For license information, please see license.txt

frappe.ui.form.on('Relacion Pacientes', {
	refresh: function(frm) {
	frm.fields_dict.ordenar_por.df.options=[
		{
        	"value": "fecha",
        	"label": "Fecha"
        },
        {
        	"value": "name",
        	"label": "Documento"
        },
        {
        	"value": "paciente",
        	"label": "Nombre"
        },
        {
        	"value": "ars_nombre",
        	"label": "ARS"
        },
	]
	frm.refresh_fields("ordernar_por")

	},
	ordernar_por: function (frm){
		frm.trigger("validate_btn");
		console.log("ordenado");
	},
	validate_btn: function(frm)
	{
		var privado=0;
		var reclamado=0;
		var diferencia=0;
		
		frappe.run_serially([
			() => frappe.dom.freeze("Un momento por favor..."),
			() => frm.call("get_consultas").done(console.log("done")),
			() => frappe.dom.unfreeze(),
		]);
		// frappe.call({
		// 	method: "consultas.consultas.doctype.relacion_pacientes.relacion_pacientes.get_consultas",
		// 	args: {
		// 		"fecha_inicial": frm.doc.fecha_inicial,
		// 		"fecha_final": frm.doc.fecha_final,
		// 		"sucursal": frm.doc.sucursal,
		// 		"facturados": frm.doc.mostrar_facturados,
		// 		"borradores": !!frm.doc.borradores,
		// 		"ordenar": frm.doc.ordernar_por,
		// 	},
		// 	callback: function(response) {
		// 		if(response) {
		// 			frappe.model.clear_table(frm.doc,"consultas");
		// 			$.each(response.message,function(key,value){
		// 				frm.add_child("consultas",{
		// 					"fecha":value.fecha,
		// 					"type":value.tipo,
		// 					"document":value.name,
		// 					"paciente":value.paciente,
		// 					"ars":value.ars_nombre,
		// 					"privado":value.privado,
		// 					"reclamado":value.reclamado,
		// 					"autorizado":value.autorizado,
		// 					"diferencia":value.diferencia
		// 				});
		// 				privado += value.privado;
		// 				reclamado += value.reclamado;
		// 				diferencia += value.diferencia;
		// 			});
		// 			frm.set_value("total_porciento_seguro",reclamado * (frm.doc.porciento_seguro/100))
		// 			frm.set_value("total_porciento_privado",privado * (frm.doc.porciento_privado/100))
		// 			frm.set_value("total_asegurados",reclamado)
		// 			frm.set_value("total_privados",privado)
		// 			frm.set_value("total_diferencias",diferencia)
		// 			frm.set_value("total_a_pagar",frm.doc.total_porciento_seguro+frm.doc.total_porciento_privado)
					
		// 			refresh_field("consultas");	
		// 		}
		// 		frappe.dom.unfreeze();
		// 	}
		// })
	}
});
