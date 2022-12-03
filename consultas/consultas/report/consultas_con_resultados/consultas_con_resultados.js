// Copyright (c) 2016, Lewin Villar and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Consultas Con Resultados"] = {
	"filters": [
		{
			"label": "Desde Fecha",
			"fieldtype": "Date",
			"fieldname": "from_date",
			"reqd": 1,
		},
		{
			"label": "Hasta Fecha",
			"fieldtype": "Date",
			"fieldname": "to_date",
			"reqd": 1,
		},
		{
			"label": __("Mostrar Pruebas?"),
			"fieldtype": "Check",
			"fieldname": "show_items",
			"default": 0,
		},
		{
			"label": __("Incluir Borradores?"),
			"fieldtype": "Check",
			"fieldname": "include_draft",
			"default": 1,
		}
	]
}
