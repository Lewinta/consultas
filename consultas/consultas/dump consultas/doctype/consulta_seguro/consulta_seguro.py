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
	
	def guardar_lista_de_precio(self):
		for row in self.pruebas:
			nombre_lista_precio = self.obtener_lista_de_precio(self.ars, row.prueba)
			if nombre_lista_precio:
				doc = frappe.get_doc("Lista Precio", nombre_lista_precio)
				doc.monto = row.diferencia
				doc.save()
				
			else:
				doc = frappe.get_doc({
					"doctype": "Lista Precio",
					"prueba": row.prueba,
					"tipo_lista": "ARS",
					"ars_medico": self.ars,
					"monto": row.autorizado
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
