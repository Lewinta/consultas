// Copyright (c) 2016, Lewin Villar and contributors
// For license information, please see license.txt

frappe.ui.form.on('ARS', {
	refresh: function(frm) {

	}
});

frappe.ui.form.on('ARS','telefono',
	function (frm)
	{
		frappe.model.set_value(frm.doctype,frm.docname,"telefono",mask_phone(frm.doc.telefono));	
	
	});
