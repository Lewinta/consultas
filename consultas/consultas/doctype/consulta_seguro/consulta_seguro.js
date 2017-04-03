// Copyright (c) 2016, Lewin Villar and contributors
// For license information, please see license.txt

frappe.ui.form.on('Consulta Seguro', {
	refresh: function(frm) {
		frappe.model.set_value(frm.doctype,frm.docname,"fecha",new Date());
	}
});

frappe.ui.form.on("Consulta Seguro", "autorizado",
         function(frm)
         {
              if(frm.doc.diferencia)
		frappe.model.set_value(frm.doctype,frm.docname,"reclamado",
		(parseFloat(frm.doc.autorizado)+parseFloat(frm.doc.diferencia)).toFixed(2));
	      else
		frappe.model.set_value(frm.doctype,frm.docname,"reclamado",parseFloat(frm.doc.autorizado));
        });

frappe.ui.form.on("Consulta Seguro", "diferencia",
         function(frm)
         {
              if(frm.doc.autorizado)
		frappe.model.set_value(frm.doctype,frm.docname,"reclamado",
		parseFloat(frm.doc.autorizado)+parseFloat(frm.doc.diferencia));
	      else
		frappe.model.set_value(frm.doctype,frm.docname,"reclamado",parseFloat(frm.doc.diferencia));
        });
frappe.ui.form.on("Consulta Seguro", "ars",
         function(frm)
  {
	frappe.call(
	{
            "method": "frappe.client.get",
            args: {
                doctype: "Ars",
                name: frm.doc.ars
           	  },
            callback: function (data) {
                console.log("Ars:"+frm.doc.ars);
		frappe.model.set_value(frm.doctype,frm.docname, "ars_nombre", data.message.nombre)
                console.log("Nombre:"+frm.message.ars_nombre);

            }
        })
 });

