// Copyright (c) 2016, Lewin Villar and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Resumen de Ventas"] = {
	"filters": [
		{
			"label": __("From Date"),
			"fieldname": "from_date",
			"fieldtype": "Date",
			"reqd": 1,
		},
		{
			"label": __("To Date"),
			"fieldname": "to_date",
			"fieldtype": "Date",
			"reqd": 1,
		},
		{
			"label": __("Sucursal"),
			"fieldname": "sucursal",
			"fieldtype": "Link",
			"options": "Empresa",
			"reqd": 1,
		},
		{
			"label": __("Nombre Sucursal"),
			"fieldname": "nombre_sucursal",
			"fieldtype": "Read Only",
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
	]
}
