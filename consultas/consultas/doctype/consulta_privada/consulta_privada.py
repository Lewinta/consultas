# -*- coding: utf-8 -*-
# Copyright (c) 2015, Lewin Villar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname

class ConsultaPrivada(Document):
	def before_insert(self):
		self.id=make_autoname("CLP-.##########")

	def validate(self):
		pruebas = [r.prueba for r in self.pruebas]
		for row in self.pruebas:
			check_duplicates(row, pruebas)
			check_price(row)
		self.calculate_totals()
	
	def guardar_lista_de_precio(self):
		self.new_inserted = False
		for row in self.pruebas:
			nombre_lista_precio = self.obtener_lista_de_precio(self.medico, row.prueba)
			if nombre_lista_precio:
				doc = frappe.get_doc("Lista Precio", nombre_lista_precio)
				doc.monto = row.diferencia
				doc.save()
				
			else:
				doc = frappe.get_doc({
					"doctype": "Lista Precio",
					"prueba": row.prueba,
					"tipo_lista": "Medico",
					"ars_medico": self.medico,
					"monto": row.diferencia
				})
				
				doc.insert()
				self.new_inserted = True
				#frappe.msgprint("Se ha agregado una Prueba nueva a la lista de {0}".format(self.medico))
				
		return self.new_inserted
		
	def obtener_lista_de_precio(self, medico, prueba):
		result = frappe.db.sql("""SELECT name 
			FROM `tabLista Precio` 
			WHERE ars_medico = '{0}' 
			AND prueba = '{1}'"""
			.format(medico, prueba),
		as_dict=True)
		
		if result:
			return result[0].name
			
		return None
	
	def calculate_totals(self):
		self.diferencia = sum([x.diferencia for x in self.pruebas])

def check_price(row):
	if row.diferencia <= .00:
		frappe.throw("""
			<p class='text-center'><b>Precio invalido</b></p><b>Prueba: </b>{prueba_nombre}<br> 
			<b>Linea:</b> {idx}
			""".format(**row.as_dict())
		)
def check_duplicates(row, pruebas):
	if pruebas.count(row.prueba) > 1:
		frappe.throw("""
		<p class='text-center'><b>Prueba duplicada</b></p><b>Prueba: </b>{prueba_nombre}<br> 
		""".format(**row.as_dict())
	)	