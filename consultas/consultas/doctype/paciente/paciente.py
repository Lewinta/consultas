# -*- coding: utf-8 -*-
# Copyright (c) 2015, Lewin Villar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname

class Paciente(Document):
	def before_insert(self):
                self.id=make_autoname("PAC-.##########")
	def before_update(self):
		#doc = frappe.get_doc("Paciente",self.id)
		#doc.name=self.nombre_completo
		#doc.save()
		self.name=self.nombre_completo
		#print(self.name)
@frappe.whitelist()
def make_consulta_privada(source_name, target_doc = None):
	doclist = get_mapped_doc("Paciente", source_name, {
		"Paciente": {
			"doctype": "Consulta Privada",
			"validation": {
				"docstatus": ["=", 0]
			}
		}
	}, target_doc)

	return doclist