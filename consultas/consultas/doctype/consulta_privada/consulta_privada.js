// Copyright (c) 2016, Lewin Villar and contributors
// For license information, please see license.txt

frappe.ui.form.on('Consulta Privada', {
	refresh: function(frm) 
	{
          frappe.model.set_value(frm.doctype,frm.docname,"fecha",new Date());    
	}
});
