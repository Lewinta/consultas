// Copyright (c) 2016, Lewin Villar and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Cierre de Ventas"] = {
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
            "fieldname":"sucursal",
            "label": __("Sucursal"),
            "fieldtype": "Link",
            "options": "Empresa",
        },
	]
}
