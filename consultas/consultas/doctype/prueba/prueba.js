// Copyright (c) 2017, Lewin Villar and contributors
// For license information, please see license.txt

frappe.ui.form.on('Prueba', {
	refresh: function(frm) {
		if(!frm.is_new()){
			frm.add_custom_button("Indice de Prueba", () => {
				frappe.set_route("List", "Indice Prueba", {"prueba":frm.doc.name})
			})
			frm.add_custom_button("Anexo", () => {
				frappe.set_route("List", "Anexo", {"prueba":frm.doc.name})
			})
		}
	},
	nombre:function(frm){
		frappe.model.set_value(frm.doctype,frm.docname,"nombre",(frm.doc.nombre).toUpperCase());
	}	
});
