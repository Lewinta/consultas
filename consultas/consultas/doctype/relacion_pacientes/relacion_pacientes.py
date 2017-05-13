# -*- coding: utf-8 -*-
# Copyright (c) 2017, Lewin Villar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class RelacionPacientes(Document):
	pass
@frappe.whitelist()
def get_consultas(fecha_inicial,fecha_final,sucursal):
	result = frappe.db.sql("""SELECT fecha,paciente,ars_nombre,privado,reclamado,autorizado,diferencia,medico,sucursal,sucursal_nombre
		FROM `viewRelacion Pacientes` 
			WHERE fecha >='{0}' AND fecha <='{1}' AND sucursal='{2}'"""
			.format(fecha_inicial,fecha_final,sucursal),
		as_dict=True)
	if result:
		return result
			
		return None
