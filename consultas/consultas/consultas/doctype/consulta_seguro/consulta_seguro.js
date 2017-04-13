// Copyright (c) 2016, Lewin Villar and contributors
// For license information, please see license.txt
frappe.ui.form.on('Consulta Seguro',
{
    refresh: function(frm)
    {
		
        if (!frm.doc.__islocal) return;
        frappe.model.set_value(frm.doctype, frm.docname, "fecha", new Date());
        var callback = function(data)
        {
            frappe.model.set_value(frm.doctype, frm.docname, "empresa", data.empresa);
        };

        frappe.model.get_value("User", frappe.session.user, "empresa", callback);
    },
	paciente:function(frm)
	{
		if (!frm.doc.pruebas||!frm.doc.ars) return;
		
		frm.doc.pruebas.forEach(function(child) {

            frappe.model.get_value("Lista Precio", {ars_medico: frm.doc.ars,prueba: child.prueba}, "monto", function(data) {
				
                if (data) {
                    child.autorizado=data.monto;
                    child.diferencia=(data.monto/0.8)*0.2;
                    child.reclamado=child.autorizado+child.diferencia;
					refresh_field("pruebas");
                } 
				else {
                    frappe.model.get_value("Prueba", child.prueba, "precio", function(dftl) {
						child.autorizado=dftl.precio*0.8;
						child.diferencia=dftl.precio*0.2;
						child.reclamado=child.autorizado+child.diferencia;
						refresh_field("pruebas");
                    });
                }
            });
        });
	},
    validate: function(frm)
    {
        frappe.model.set_value(frm.doctype, frm.docname, "responsable", frappe.session.user);
    },
	before_submit:function(frm)
	{
			if (!frm.doc.autorizacion)
			{	
				frappe.throw("Debes agregar el numero de autorizacion antes de guardar el documento");
				validated=false;
				return ;
			}	
            var callback = function(data) {
                //console.log(data);
                return;
            }
            
			frm.doc.pruebas.forEach(function(child) {

				frappe.model.get_value("Lista Precio", {
						prueba: child.prueba,
						ars_medico: frm.doc.medico
					},
					"monto",
					callback);
			});
			
			console.log("runserverobj");
			$c('runserverobj', {"method": "guardar_lista_de_precio", "docs": cur_frm.doc}, function(response){
				if(response.message){
					frappe.show_alert("Se ha agregado una Prueba nueva a la lista de Precio de " + frm.doc.ars,15);
				}
			});
	},
    ars: function(frm)
    {
        frappe.call(
        {
            "method": "frappe.client.get",
            args:
            {
                doctype: "ARS",
                name: cur_frm.doc.ars
            },
            callback:function(data)
            {
                frappe.model.set_value(frm.doctype, frm.docname, "ars_nombre", data.message.nombre);
            }
        });
    }
});


frappe.ui.form.on("Consulta Prueba",
{	prueba:
	function(frm,cdt,cdn)
	{
		var tAutorizado=0,tDiferencia=0,tReclamado=0;
		var row = locals[cdt][cdn];
		
		var busca_precio = function(data) {
            
			if (data) //El precio esta en la lista de precios del medico o ARS
            {
                frappe.model.set_value(cdt, cdn, "autorizado", data.monto);
				frappe.model.set_value(cdt,cdn,"diferencia",(data.monto/0.8)*0.2);
				frappe.model.set_value(cdt,cdn,"reclamado",row.autorizado+row.diferencia);
				
				
            } else //Tomamos el precio por defecto
            {
                frappe.model.get_value("Prueba", row.prueba,"precio",function(data){
					frappe.model.set_value(cdt,cdn,"autorizado",data.precio*0.8);
					frappe.model.set_value(cdt,cdn,"diferencia",data.precio*0.2);
					frappe.model.set_value(cdt,cdn,"reclamado",data.precio);
			
					frm.doc.pruebas.forEach(function(child){
						if (child.autorizado) tAutorizado+=child.autorizado;
						if (child.diferencia) tDiferencia+=child.diferencia;
						if (child.reclamado) tReclamado+=child.reclamado;
						frappe.model.set_value(frm.doctype,frm.docname,"autorizado",tAutorizado);
						frappe.model.set_value(frm.doctype,frm.docname,"reclamado",tReclamado);
						frappe.model.set_value(frm.doctype,frm.docname,"diferencia",tDiferencia);	
					});	
				});
            }
            
        }

		if (row.prueba)frappe.model.get_value("Lista Precio", {ars_medico: frm.doc.ars,prueba: row.prueba},"monto", busca_precio);
		else frm.get_field("pruebas").grid.grid_rows[row.idx-1].remove();
		 
		
	},
	autorizado:
	function(frm,cdt,cdn)
	{
		var tAutorizado=0,tDiferencia=0,tReclamado=0;
		var row = locals[cdt][cdn];
		frappe.model.set_value(cdt,cdn,"reclamado",row.autorizado+row.diferencia);
		
		frm.doc.pruebas.forEach(function(child){
			if (child.autorizado) tAutorizado+=child.autorizado;
			if (child.diferencia) tDiferencia+=child.diferencia;
			if (child.reclamado) tReclamado+=child.reclamado;
			
			frappe.model.set_value(frm.doctype,frm.docname,"autorizado",tAutorizado);
			frappe.model.set_value(frm.doctype,frm.docname,"reclamado",tReclamado);
			frappe.model.set_value(frm.doctype,frm.docname,"diferencia",tDiferencia);	
		});	
	},
	diferencia:
	function(frm,cdt,cdn)
	{
		var tAutorizado=0,tDiferencia=0,tReclamado=0;
		var row = locals[cdt][cdn];
		frappe.model.set_value(cdt,cdn,"reclamado",row.autorizado+row.diferencia);
		frm.doc.pruebas.forEach(function(child){
			if (child.autorizado) tAutorizado+=child.autorizado;
			if (child.diferencia) tDiferencia+=child.diferencia;
			if (child.reclamado) tReclamado+=child.reclamado;
			frappe.model.set_value(frm.doctype,frm.docname,"autorizado",tAutorizado);
			frappe.model.set_value(frm.doctype,frm.docname,"reclamado",tReclamado);
			frappe.model.set_value(frm.doctype,frm.docname,"diferencia",tDiferencia);	
		});	
	}
});