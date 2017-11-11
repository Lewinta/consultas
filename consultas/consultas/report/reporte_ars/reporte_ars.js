// Copyright (c) 2016, Lewin Villar and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Reporte ARS"] = {
	"filters": [
		{
            "fieldname":"fecha_inicial",
            "label": __("Fecha Inicial"),
            "fieldtype": "Date",
            "options": "",
        },
		{
            "fieldname":"fecha_final",
            "label": __("Fecha Final"),
            "fieldtype": "Date",
            "options": "",
        },
        {
            "fieldname":"paciente",
            "label": __("Paciente"),
            "fieldtype": "Link",
            "options": "Paciente",
        },
		{
            "fieldname":"ars",
            "label": __("ARS"),
            "fieldtype": "Link",
            "options": "ARS",
        },
		{
            "fieldname":"sucursal",
            "label": __("Sucursal"),
            "fieldtype": "Link",
            "options": "Empresa",
        },
		{
            "fieldname":"autorizacion",
            "label": __("Autorizacion"),
            "fieldtype": "Data",
        },
	]
}


frappe.provide("frappe.views");
frappe.views.GridReport = Class.extend({
	init: function(opts) {
		console.log("data")
	}
});