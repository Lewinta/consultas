// Copyright (c) 2017, Lewin Villar and contributors
// For license information, please see license.txt

frappe.ui.form.on('Prueba', {
	refresh: function(frm) {

	},
	nombre:function(frm){
		frappe.model.set_value(frm.doctype,frm.docname,"nombre",(frm.doc.nombre).toUpperCase());
	}	
});
