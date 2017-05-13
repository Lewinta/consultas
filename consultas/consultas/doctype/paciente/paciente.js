// Copyright (c) 2016, Lewin Villar and contributors
// For license information, please see license.txt

frappe.ui.form.on('Paciente', {
	refresh: function(frm) {
		frappe.model.set_value(frm.doctype,frm.docname,"responsable",frappe.session.user);	
	},
	telefono:function(frm){
        frappe.model.set_value(frm.doctype,frm.docname, "telefono",mask_phone(frm.doc.telefono));
    },
	nombre:function(frm){
		var name=frm.doc.nombre.trim();	
		
		frappe.model.set_value(frm.doctype,frm.docname,"nombre",(name).toUpperCase());
		
		//frappe.model.set_value(frm.doctype,frm.docname, "nombre",frm.doc.nombre);	
		//refresh_field("nombre");
		if(frm.doc.apellido)
			frappe.model.set_value(frm.doctype,frm.docname, "nombre_completo",frm.doc.nombre+" "+frm.doc.apellido);
		else
			frappe.model.set_value(frm.doctype,frm.docname, "nombre_completo",frm.doc.nombre);	
	},
	apellido:function(frm)
	{
		var name=frm.doc.apellido.trim();	
		
		frappe.model.set_value(frm.doctype,frm.docname,"apellido",(name).toUpperCase());
		refresh_field("apellido");
		frappe.model.set_value(frm.doctype,frm.docname,"apellido",(frm.doc.apellido).toUpperCase());
		if(frm.doc.nombre)
			frappe.model.set_value(frm.doctype,frm.docname, "nombre_completo",frm.doc.nombre+" "+frm.doc.apellido);
		else
			frappe.model.set_value(frm.doctype,frm.docname, "nombre_completo",frm.doc.apellido);
	},
	direccion:function(frm)
	{
		frappe.model.set_value(frm.doctype,frm.docname,"direccion",(frm.doc.direccion).toUpperCase());
	},
	correo_electronico:function(frm)
	{
		frappe.model.set_value(frm.doctype,frm.docname,"correo_electronico",(frm.doc.correo_electronico).toLowerCase());
	},
	add_toolbar_buttons: function(frm) {	
		if (frm.doc.status == "Approved") {
			frm.add_custom_button(__('Customer Loan'), function() {
				frappe.call({
					type: "GET",
					method: "fm.finance_manager.doctype.loan_application.loan_application.make_loan",
					args: {
						"source_name": frm.doc.name
					},
					callback: function(r) {
						if(!r.exc) {
							var doc = frappe.model.sync(r.message);
							frappe.set_route("Form", r.message.doctype, r.message.name);
						}
					}
				});
			})
		}
	}
});


function mask_phone(phone)
{
        var pattern =new RegExp("((^[0-9]{3})[0-9]{3}[0-9]{4})$");
        var pattern1 =new RegExp("([(][0-9]{3}[)] [0-9]{3}-[0-9]{4})$");
        var pattern2 =new RegExp("([(][0-9]{3}[)][0-9]{3}-[0-9]{4})$");

        if(pattern.test(phone))
                return ("({0}{1}{2}) {3}{4}{5}-{6}{7}{8}{9}".format(phone));
        else if(pattern1.test(phone))
                return phone;
        else if(pattern2.test(phone))
                return ("{0}{1}{2}{3}{4} {5}{6}{7}{8}{9}{10}{11}{12}".format(phone));


}


