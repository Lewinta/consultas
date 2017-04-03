// Copyright (c) 2016, Lewin Villar and contributors
// For license information, please see license.txt

frappe.ui.form.on('Paciente', {
	refresh: function(frm) {

	}
});

frappe.ui.form.on("Paciente", "telefono",
    function(frm)
	 {
        	frappe.model.set_value(frm.doctype,frm.docname, "telefono",mask_phone(frm.doc.telefono));
	});

frappe.ui.form.on("Paciente", "nombre",
    function(frm)
 {
    if(frm.doc.apellido)
        frappe.model.set_value(frm.doctype,frm.docname, "nombre_completo",frm.doc.nombre+" "+frm.doc.apellido);
    else
        frappe.model.set_value(frm.doctype,frm.docname, "nombre_completo",frm.doc.nombre);
});

frappe.ui.form.on("Paciente", "apellido",
    function(frm)
 {
    if(frm.doc.nombre)
        frappe.model.set_value(frm.doctype,frm.docname, "nombre_completo",frm.doc.nombre+" "+frm.doc.apellido);
    else
        frappe.model.set_value(frm.doctype,frm.docname, "nombre_completo",frm.doc.apellido);
 });

