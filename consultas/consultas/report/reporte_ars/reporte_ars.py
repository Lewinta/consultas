# Copyright (c) 2013, Lewin Villar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	fields = ["paciente","ars_nombre","diferencia","reclamado","autorizado","medico"]
	filters = {"name":"CLS-0000001795"}

	result = frappe.get_list("Consulta Seguro",fields,filters)
	columns, data = [" ","Paciente","ARS Nombre","Diferencia","Monto Reclamado","Monto Autorizado","Medico"], []
	data.extend(result or [])
	frappe.msgprint(data)
	return columns, data