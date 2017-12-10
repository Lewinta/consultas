frappe.listview_settings["Paciente"] = {
	"refresh": function(list) {
		list.page.fields_dict.nombre_completo.df.read_only = 0;
		list.page.fields_dict.nombre_completo.df.fieldtype = "Data";
	}
}