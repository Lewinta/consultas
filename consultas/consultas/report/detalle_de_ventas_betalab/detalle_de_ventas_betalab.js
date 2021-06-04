// Copyright (c) 2016, Lewin Villar and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Detalle de Ventas Betalab"] = {
	"filters": [
		{
			"label": __("From Date"),
			"fieldname": "from_date",
			"fieldtype": "Date",
			"default": frappe.datetime.year_start(),
			"reqd": 1,
		},
		{
			"label": __("To Date"),
			"fieldname": "to_date",
			"fieldtype": "Date",
			"default": frappe.datetime.year_end(),
			"reqd": 1,
		},
		// {
		// 	"label": __("Sucursal"),
		// 	"fieldname": "sucursal",
		// 	"fieldtype": "Link",
		// 	"options": "Empresa",
		// 	"reqd": 1,
		// },
		{
			"label": __("Prueba"),
			"fieldname": "prueba",
			"fieldtype": "Link",
			"options": "Prueba",
			"reqd": 1,
		},
		{
			"label": __("Tipo de Consulta"),
			"fieldname": "tipo_de_consulta",
			"fieldtype": "Select",
			"options": "\nConsulta Privada\nConsulta Seguro",
		},
		{
			"label": __("Team"),
			"fieldname": "team",
			"fieldtype": "Link",
			"options": "Institucion",
		},
	],
	formatter: function (row, cell, value, columnDef, dataContext, default_formatter) {
		value = default_formatter(row, cell, value, columnDef, dataContext);
		
		if (cell == 1) {
			let dt = dataContext['Documento'].split("-")[0] == "CLP" ? "Consulta Privada" : "Consulta Seguro" ;
			value = `<a class="grey" target="_blank" href="#Form/${dt}/${dataContext['Documento']}">${dataContext['Documento']}</a>`;
		}

		return value;
	}
}
