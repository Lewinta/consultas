# -*- coding: utf-8 -*-
# Copyright (c) 2017, Lewin Villar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class RelacionPacientes(Document):
	pass
@frappe.whitelist()
def get_consultas(fecha_inicial,fecha_final,sucursal,borradores):
	docstatus = "0,1" if borradores else "1" 
	result = frappe.db.sql("""SELECT fecha,name,tipo,paciente,ars_nombre,privado,reclamado,autorizado,diferencia,medico,sucursal,sucursal_nombre,docstatus
		FROM `viewRelacion Pacientes` 
			WHERE fecha >='{0}' AND fecha <='{1}' AND sucursal='{2}' AND docstatus in ({3})"""
			.format(fecha_inicial,fecha_final,sucursal,docstatus),
		as_dict=True)
	frappe.msgprint("done")
	if result:
		return result
			
		return None
