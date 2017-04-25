// Copyright (c) 2017, Lewin Villar and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tipo Prueba', {
	refresh: function(frm) {

	},
	tipo:function(frm){
		frappe.model.set_value(frm.doctype,frm.docname,"tipo",(frm.doc.tipo).toUpperCase());
	}
});
