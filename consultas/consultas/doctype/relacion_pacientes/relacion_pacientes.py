# -*- coding: utf-8 -*-
# Copyright (c) 2017, Lewin Villar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import flt

class RelacionPacientes(Document):
	def get_consultas(self):
		self.total_porciento_seguro = .000
		self.total_asegurados 		= .000
		self.total_privados 		= .000
		self.total_diferencias 		= .000
		self.total_a_pagar 			= .000
		self.consultas = []
		docstatus = "0,1" if self.borradores else "1" 

		result = frappe.db.sql("""SELECT fecha, name as document, tipo as type, paciente, ars_nombre as ars, privado, reclamado, autorizado, diferencia
			FROM `viewRelacion Pacientes` 
				WHERE fecha >='{0}' AND fecha <='{1}' AND sucursal='{2}' AND docstatus in ({3}) AND facturado = {4} ORDER BY {5} """
				.format(self.fecha_inicial, self.fecha_final, self.sucursal, docstatus, self.mostrar_facturados, self.ordenar_por), debug=False, as_dict=True)
		# frappe.msgprint("Consultas Generadas")
		if not result:
			frappe.msgprint("No se encontraron consultas con los criterios de busqueda seleccionados")

		for consulta in result:
			self.append("consultas", consulta)
			# ok let's update the totals
			self.total_privados     += consulta.privado
			self.total_asegurados   += consulta.reclamado
			self.total_diferencias  += consulta.diferencia
		self.total_porciento_seguro  = flt(self.total_asegurados) * flt(self.porciento_seguro) / 100.0
		self.total_porciento_privado = flt(self.total_privados) * flt(self.porciento_privado) / 100.0
		self.total_a_pagar = flt(self.total_porciento_seguro) + flt(self.total_porciento_privado)

	
@frappe.whitelist()
def get_consultas(fecha_inicial, fecha_final, sucursal, borradores, facturados, ordenar="fecha"):
	frappe.errprint(borradores)
	docstatus = "0,1" if borradores else "1" 
	result = frappe.db.sql("""SELECT fecha,name,tipo,paciente,ars_nombre,privado,reclamado,autorizado,diferencia,medico,sucursal,sucursal_nombre,docstatus
		FROM `viewRelacion Pacientes` 
			WHERE fecha >='{0}' AND fecha <='{1}' AND sucursal='{2}' AND docstatus in ({3}) AND facturado = {4} ORDER BY {5} """
			.format(fecha_inicial,fecha_final,sucursal,docstatus, facturados, ordenar), debug=True, as_dict=True)
	frappe.msgprint("Consultas Generadas")
	if result:
		return result		
