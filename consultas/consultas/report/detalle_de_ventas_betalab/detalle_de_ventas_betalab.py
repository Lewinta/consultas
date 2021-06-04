# Copyright (c) 2013, Lewin Villar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt

def execute(filters=None):
	return get_columns(), get_data(filters)

def get_columns():
	columns = [
		"Documento:Data:120",
		"Tipo:Data:120",
		"Fecha:Date:100",
		"Sucursal:Data:220",
		"Paciente:Data:200",
		"Precio:Currency:120",
	]

	return columns

def get_conditions(filters):

	conditions = ["v.docstatus in (0,1)"]

	
	if filters.get("tipo_de_consulta"):
		conditions.append("v.tipo_de_consulta = '{}'".format(filters.get("tipo_de_consulta")))
	# if filters.get("sucursal"):
	conditions.append("v.sucursal  in ('EMP-000006', 'EMP-000014', 'EMP-000012', 'EMP-000018', 'EMP-000003')")
	
	if filters.get("prueba"):
		conditions.append("v.prueba = '{}'".format(filters.get("prueba")))	
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
	return frappe.db.sql("""
		SELECT 
			v.parent, 
			v.tipo_de_consulta,
			v.fecha,
			v.sucursal_nombre,
			v.paciente,
			v.monto
		FROM 
			`viewVentas Por Prueba` v
		WHERE 
			{conditions}
		GROUP BY 
			v.parent
		ORDER BY 
			v.fecha
		""".format(conditions=conditions), debug=True)

	