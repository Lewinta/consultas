// Copyright (c) 2016, Lewin Villar and contributors
// For license information, please see license.txt

frappe.ui.form.on('Paciente', {
	
	refresh: function(frm) {
		frappe.model.set_value(frm.doctype,frm.docname,"responsable",frappe.session.user);
		frm.trigger("add_toolbar_buttons")	
	},
	after_save: function(frm) {
		if(frm.doc.name != frm.doc.nombre_completo){
			var doctype = cur_frm.doctype;
			var docname = cur_frm.docname;
			var old_name = cur_frm.docname;
			var new_name = cur_frm.doc.nombre_completo;

			frappe.call({
				method: "frappe.model.rename_doc.rename_doc",
				args: {
					"doctype": doctype,
					"old": old_name,
					"new": new_name,
					"merge": false
				},
				callback: function callback(r, rt) {
					if (!r.exc) {
						$(document).trigger('rename', [doctype, docname, r.message || new_name]);
						if (locals[doctype] && locals[doctype][docname]) delete locals[doctype][docname];

					}
				}
			});
		}

	},
	validate: function(frm){
		if( frm.doc.sexo == "-")
		{
			frappe.msgprint("Debes seleccionar el sexo")
			validate = false
			return
		}

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
	make_consulta: function(frm) {
		
		// the args that it requires
		var args = {
			"source_name": frm.doc.name,
			"tipo_consulta": frm.doc._tipo_consulta
		}

		// callback to be executed after the server responds
		var callback = function(response) {

			// check to see if there is something back
			if (!response.message) 
				return 1 // exit code is 1

			var doc = frappe.model.sync(response.message)
			frappe.set_route("Form", response.message.doctype, response.message.name)
		}

		frappe.call({ "method": frm.doc._temp_consulta, "args": args, "callback": callback })
	},
	add_toolbar_buttons: function(frm) {
				
		var consulta_privada = function(){
			frm.doc._tipo_consulta = "Consulta Privada"
			//set the method to be call on make_consulta
			frm.doc._temp_consulta = "consultas.consultas.doctype.paciente.paciente.make_consulta"
			frm.trigger("make_consulta")
		}
		var consulta_seguro = function(){
			frm.doc._tipo_consulta = "Consulta Seguro"
			//set the method to be call on make_consulta
			frm.doc._temp_consulta = "consultas.consultas.doctype.paciente.paciente.make_consulta"
			frm.trigger("make_consulta")
		}
		var calcula_edad = function(){
			
			var fields = [{
				"fieldname": "fecha_nacimiento",
				"fieldtype": "Date",
				"label": "Fecha de Nacimiento",
				"default": frappe.datetime.get_today()
			}]

			var onsubmit = function(values){
				
				var days = frappe.datetime.get_diff(frappe.datetime.get_today(), values.fecha_nacimiento)
				cur_frm.set_value("edad",parseInt(days/365))
			}
 
			frappe.prompt(fields,onsubmit,'Calcular Edad del Paciente','Calcular')
		}

		frm.add_custom_button(__('Calcular Edad' ), calcula_edad)
		frm.add_custom_button(__('Consulta Privada'), consulta_privada, "Crear")
		frm.add_custom_button(__('Consulta Seguro' ), consulta_seguro,  "Crear")
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


