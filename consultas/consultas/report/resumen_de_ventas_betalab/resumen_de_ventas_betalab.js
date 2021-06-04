// Copyright (c) 2016, Lewin Villar and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Resumen de Ventas Betalab"] = {
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
	]
}
