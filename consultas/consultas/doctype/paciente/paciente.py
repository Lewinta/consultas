# -*- coding: utf-8 -*-
# Copyright (c) 2015, Lewin Villar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.model.naming import make_autoname

class Paciente(Document):
	
	def before_insert(self):
		self.web_hash = frappe.generate_hash("Paciente",10)
		# self.name = make_autoname("PAC-.#####")
		# self.insert()
		# frappe.db.commit()	
		
	# def save(self):
		# pass
		#doc = frappe.get_doc("Paciente",self.id)
		#doc.name=self.nombre_completo
		#frappe.errprint("old {0} new {1}".format(self.name,self.nombre_completo))
		#self.name=self.nombre_completo
		#frappe.errprint("old {0} new {1}".format(self.name,self.nombre_completo))
		# self.update()
		#print(self.name)

@frappe.whitelist()
def make_consulta(source_name,tipo_consulta ,target_doc = None):
	consulta = get_mapped_doc("Paciente", source_name, {
		"Paciente": {
			"doctype": tipo_consulta,
			"validation": {
				
			}
		}
	}, target_doc)

	return consulta
