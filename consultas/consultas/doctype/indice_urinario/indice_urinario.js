// Copyright (c) 2017, Lewin Villar and contributors
// For license information, please see license.txt

frappe.ui.form.on('Indice Urinario', {
	refresh: function(frm) {

	},
	opciones: frm => {
		if (frm.doc.opciones)
			frm.set_value("opciones", frm.doc.opciones.toUpperCase());
	}
});
