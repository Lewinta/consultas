# Copyright (c) 2013, Lewin Villar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt

def execute(filters=None):
	return get_columns(filters), get_data_with_items(filters) if filters.get("show_items") else get_data(filters)

def get_columns(filters):
	columns = [
		"Resultado:Link/Resultado:120",
		"Fecha Res.:Date:100",
		"Estado:Data:80",
		"Paciente:Data:250",
		"Sucursal:Data:120",
		"Tipo Consulta:Data:150",
		"Consulta:Data:130",
		"Fecha Cons.:Date:100",
		"Reclamado:Currency:120",
		"Autorizado:Currency:120",
		"Diferencia:Currency:120",
	]

	columns_with_items = [
		"Resultado:Link/Resultado:120",
		"Fecha Res.:Date:100",
		"Estado:Data:80",
		"Paciente:Data:250",
		"Sucursal:Data:120",
		"Tipo Consulta:Data:150",
		"Consulta:Data:130",
		"Fecha Cons.:Date:100",
		"Prueba:Data:180",
		"Prueba Nombre:Data:200",
		"Reclamado:Currency:120",
		"Autorizado:Currency:120",
		"Diferencia:Currency:120",
	]

	return columns_with_items if filters.get("show_items") else columns

def get_conditions(filters):
	conditions = []

	if filters.get("from_date"):
		conditions.append("`tabResultado`.fecha >= '{}'".format(filters.get("from_date")))

	if filters.get("to_date"):
		conditions.append("`tabResultado`.fecha <= '{}'".format(filters.get("to_date")))

	if filters.get("include_draft"):
		conditions.append("`tabResultado`.docstatus <= 1")
	else:
		conditions.append("`tabResultado`.docstatus = 1")

	return " AND ".join(conditions)

def get_data_with_items(filters):
	conditions = get_conditions(filters)
	results = []
	return frappe.db.sql("""
		SELECT 
			`tabResultado`.name,
			`tabResultado`.fecha,
			IF(`tabResultado`.docstatus = 0, 'Borrador', 'Validado'),
			`tabResultado`.paciente,
			`tabResultado`.sucursal_nombre,
			`tabResultado`.consulta_tipo,
			`tabResultado`.consulta,
			`tabConsulta Privada`.fecha,
			`tabConsulta Prueba Privada`.prueba,
			`tabConsulta Prueba Privada`.prueba_nombre,
			0 as reclamado,
			0 as autorizado,
			`tabConsulta Prueba Privada`.diferencia
		FROM 
			`tabResultado`
		JOIN
			`tabConsulta Privada`
		ON
			`tabResultado`.consulta = `tabConsulta Privada`.name
		JOIN
			`tabConsulta Prueba Privada`
		ON
			`tabConsulta Privada`.name = `tabConsulta Prueba Privada`.parent
		WHERE 
			{conditions}
		
		UNION
		
		SELECT 
			`tabResultado`.name,
			`tabResultado`.fecha,
			IF(`tabResultado`.docstatus = 0, 'Borrador', 'Validado'),
			`tabResultado`.paciente,
			`tabResultado`.sucursal_nombre,
			`tabResultado`.consulta_tipo,
			`tabResultado`.consulta,
			`tabConsulta Seguro`.fecha,
			`tabConsulta Prueba`.prueba,
			`tabConsulta Prueba`.prueba_nombre,
			`tabConsulta Prueba`.reclamado,
			`tabConsulta Prueba`.autorizado,
			`tabConsulta Prueba`.diferencia
		FROM 
			`tabResultado`
		JOIN
			`tabConsulta Seguro`
		ON
			`tabResultado`.consulta = `tabConsulta Seguro`.name
		JOIN
			`tabConsulta Prueba`
		ON
			`tabConsulta Seguro`.name = `tabConsulta Prueba`.parent
		WHERE 
			{conditions}

		""".format(conditions=conditions), debug=True)

def get_data(filters):
	conditions = get_conditions(filters)
	results = []
	return frappe.db.sql("""
		SELECT 
			`tabResultado`.name,
			`tabResultado`.fecha,
			IF(`tabResultado`.docstatus = 0, 'Borrador', 'Validado'),
			`tabResultado`.paciente,
			`tabResultado`.sucursal_nombre,
			`tabResultado`.consulta_tipo,
			`tabResultado`.consulta,
			`tabConsulta Privada`.fecha,
			0 as reclamado,
			0 as autorizado,
			`tabConsulta Privada`.diferencia
		FROM 
			`tabResultado`
		JOIN
			`tabConsulta Privada`
		ON
			`tabResultado`.consulta = `tabConsulta Privada`.name
		WHERE 
			{conditions}
		
		UNION
		
		SELECT 
			`tabResultado`.name,
			`tabResultado`.fecha,
			IF(`tabResultado`.docstatus = 0, 'Borrador', 'Validado'),
			`tabResultado`.paciente,
			`tabResultado`.sucursal_nombre,
			`tabResultado`.consulta_tipo,
			`tabResultado`.consulta,
			`tabConsulta Seguro`.fecha,
			`tabConsulta Seguro`.reclamado,
			`tabConsulta Seguro`.autorizado,
			`tabConsulta Seguro`.diferencia
		FROM 
			`tabResultado`
		JOIN
			`tabConsulta Seguro`
		ON
			`tabResultado`.consulta = `tabConsulta Seguro`.name
		WHERE 
			{conditions}

		""".format(conditions=conditions), debug=True)

