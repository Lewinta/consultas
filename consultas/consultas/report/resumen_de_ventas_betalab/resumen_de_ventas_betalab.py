# Copyright (c) 2013, Lewin Villar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt

def execute(filters=None):
	return get_columns(), get_data(filters)

def get_columns():
	columns = [
		"Prueba:Link/Prueba:150",
		"Nombre:Data:200",
		"Cantidad:Int:100",
		"Monto:Currency:120",
		"Total:Currency:120",
		"Promedio:Currency:100",
		"% Cant.:Data:90",
		"% Total:Data:90",
	]

	return columns

def get_conditions(filters):

	conditions = ["v.docstatus in (0,1)"]

	
	if filters.get("tipo_de_consulta"):
		conditions.append("v.tipo_de_consulta = '{}'".format(filters.get("tipo_de_consulta")))
	# if filters.get("sucursal"):
	conditions.append("v.sucursal  in ('EMP-000006', 'EMP-000014', 'EMP-000012', 'EMP-000018', 'EMP-000003')")
	
	if filters.get("from_date"):
		conditions.append("v.fecha >= '{}'".format(filters.get("from_date")))
	if filters.get("to_date"):
		conditions.append("v.fecha <= '{}'".format(filters.get("to_date")))
	if filters.get("team"):
		conditions.append("v.team = '{}'".format(filters.get("team")))
	
	return " AND ".join(conditions)

def get_data(filters):
	conditions = get_conditions(filters)
	results = []
	data = frappe.db.sql("""
		SELECT 
			v.prueba, 
			v.prueba_nombre,
			v.monto,
			SUM(1) as qty, 
			SUM(v.monto) as total_prueba
		FROM 
			`viewVentas Por Prueba` v
		WHERE 
			{conditions}
		GROUP BY 
			v.prueba
		ORDER BY 
			qty desc
		""".format(conditions=conditions), debug=True, as_dict=True)

	grand_total = sum([x.total_prueba for x in data])
	grand_qty = sum([x.qty for x in data])

	for row in data:
		promedio = flt(row.total_prueba / row.qty, 2)
		results.append(
			(
				row.prueba,
				row.prueba_nombre,
				row.qty,
				row.monto, 
				row.total_prueba,
				promedio,
				"{}%".format(flt(row.qty / grand_qty * 100, 2) if grand_qty else .000),
				"{}%".format(flt(row.total_prueba / grand_total * 100, 2) if grand_total else .000)
			)
		)

	return results