// Copyright (c) 2016, Lewin Villar and contributors
// For license information, please see license.txt
frappe.ui.form.on('Consulta Seguro',
{
    onload: function(frm)
    {
        if (!frm.doc.__islocal) return;
        frappe.model.set_value(frm.doctype, frm.docname, "fecha", new Date());
        var callback = function(data)
        {
            frappe.model.set_value(frm.doctype, frm.docname, "empresa", data.empresa);
        };
        $('[data-fieldname="ars"]').hide();

        frappe.model.get_value("User", frappe.session.user, "empresa", callback);
    },
    refresh: function(frm){
    	//	frm.trigger("add_toolbar_buttons")
    	frm.add_fetch("paciente", "edad", "edad");
    },
	paciente:function(frm)
	{

		frappe.model.get_value("Paciente",{"name":frm.doc.paciente},"ars",function(data){
			if(data)
			{	
				frm.set_value("ars",data.ars)}
			if (frm.doc.pruebas){
				frm.doc.pruebas.forEach(function(child) {

		            frappe.model.get_value("Lista Precio", {ars_medico: data.ars,prueba: child.prueba}, "monto", function(response) {
						
		                if (response) {
		                    child.autorizado=response.monto * 0.8;
		                    child.diferencia=response.monto * 0.2;
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
		    }
	    }) 
	},
	autorizacion: function(frm)
	{
		cur_frm.set_value("autorizacion",(frm.doc.autorizacion).toUpperCase());
	},
    validate: function(frm)
    {
        var autorizacion =" ";
        frappe.model.set_value(frm.doctype, frm.docname, "responsable", frappe.session.user);
        if(frm.doc.autorizacion )
        {
        	autorizacion = (frm.doc.autorizacion.trim()).substring(0,1).toUpperCase();	 
        	if(frm.doc.ars == "ARS-000004" && autorizacion != "P" )
        	{
        		frappe.msgprint("Las Autorizaciones de " + frm.doc.ars_nombre + " Comienzan con 'P' verifique la ARS por favor!")
        		validated = false;
        		return false
        	}
        	else if(frm.doc.ars == "ARS-000002" && autorizacion != "H" )
        	{
        		frappe.msgprint("Las Autorizaciones de " + frm.doc.ars_nombre + " Comienzan con 'H' verifique la ARS por favor!")
        		validated = false;
        		return false
        	}
        	else 
        	{
        		validated = true;
        		return true;
        	}
        }
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
			
			$c('runserverobj', {"method": "guardar_lista_de_precio", "docs": frm.doc}, function(response){
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
                name: frm.doc.ars
            },
            callback:function(data)
            {
                frappe.model.set_value(frm.doctype, frm.docname, "ars_nombre", data.message.nombre);
            }
        });
    },
    hacer_resultado: function(frm){

    	var method	= "consultas.consultas.doctype.consulta_seguro.consulta_seguro.make_resultado"
    		// the args that it requires
		var args = {
			"source_name": frm.doc.name,
			"tipo_consulta": frm.doctype
		}

		// callback to be executed after the server responds
		var callback = function(response) {

			// check to see if there is something back
			if (!response.message) 
				return 1 // exit code is 1

			var doc = frappe.model.sync(response.message)
			frappe.set_route("Form", response.message.doctype, response.message.name)
		}

		frappe.call({ "method": method, "args": args, "callback": callback })
    },
    add_toolbar_buttons: function(frm){

		var callback = function(data){

			if(data)
		  		frappe.set_route("Form","Resultado",data.name)

		  	else
		  		frm.trigger("hacer_resultado")

		} 
		
		var resultado = function(){
    			frappe.model.get_value("Resultado", { "consulta": frm.doc.name }, "name", callback)
		}

    	frm.add_custom_button("Resultado",resultado	)
    }
});


frappe.ui.form.on("Consulta Prueba",
{	
	prueba:function(frm,cdt,cdn)
	{
		var tAutorizado=0,tDiferencia=0,tReclamado=0;
		var row = locals[cdt][cdn];
		
		var busca_precio = function(data) {
            
			if (data) //El precio esta en la lista de precios del medico o ARS
            {
                frappe.model.set_value(cdt, cdn, "reclamado", data.monto);
				frappe.model.set_value(cdt,cdn,"autorizado",data.monto * 0.8);
				frappe.model.set_value(cdt,cdn,"diferencia",data.monto * 0.2);
				
				
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
	autorizado:function(frm,cdt,cdn)
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
	diferencia:	function(frm,cdt,cdn)
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
	pruebas_remove:function(frm,cdt,cdn)
	{
		var tAutorizado=0,tDiferencia=0,tReclamado=0;
		if(frm.doc.pruebas.length > 0){

			frm.doc.pruebas.forEach(function(child){
				if (child.autorizado) tAutorizado += child.autorizado;
				if (child.diferencia) tDiferencia += child.diferencia;
				if (child.reclamado) tReclamado += child.reclamado;
				frappe.model.set_value(frm.doctype,frm.docname, "autorizado", tAutorizado);
				frappe.model.set_value(frm.doctype,frm.docname, "reclamado", tReclamado);
				frappe.model.set_value(frm.doctype,frm.docname, "diferencia", tDiferencia);
			});	
		}else{
			frappe.model.set_value(frm.doctype, frm.docname, "autorizado", 0);
			frappe.model.set_value(frm.doctype, frm.docname, "reclamado", 0);
			frappe.model.set_value(frm.doctype, frm.docname, "diferencia", 0);
		}

	}
});
