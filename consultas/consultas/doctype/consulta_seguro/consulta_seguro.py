# -*- coding: utf-8 -*-
# Copyright (c) 2015, Lewin Villar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname

class ConsultaSeguro(Document):
	def before_insert(self):
				self.id=make_autoname("CLS-.##########")
	def before_cancel(self):
		#Remove authorizations of cancelled documents to acoid diplicity
		self.autorizacion = ""
		self.db_update()
	def guardar_lista_de_precio(self):
		self.new_inserted = False
		for row in self.pruebas:
			nombre_lista_precio = self.obtener_lista_de_precio(self.ars, row.prueba)
			if nombre_lista_precio:
				doc = frappe.get_doc("Lista Precio", nombre_lista_precio)
				doc.monto = row.reclamado
				frappe.errprint("Monto [ ${0} ]  -> Reclamado [ ${1}] ".format(doc.monto,row.reclamado))
				doc.save()
				
			else:
				doc = frappe.get_doc({
					"doctype": "Lista Precio",
					"prueba": row.prueba,
					"tipo_lista": "ARS",
					"ars_medico": self.ars,
					"monto": row.reclamado
				})
				
				doc.insert()
				self.new_inserted = True
				
		return self.new_inserted
		
	def obtener_lista_de_precio(self, ars, prueba):
		result = frappe.db.sql("""SELECT name 
			FROM `tabLista Precio` 
			WHERE ars_medico = '{0}' 
			AND prueba = '{1}'"""
			.format(ars, prueba),
		as_dict=True)
		
		if result:
			return result[0].name
			
		return None

@frappe.whitelist()
def make_resultado(source_name, tipo_consulta, target_doc = None):
	resultado = frappe.new_doc("Resultado")
	resultado.consulta_tipo = tipo_consulta	
	resultado.consulta = source_name	

	return resultado
