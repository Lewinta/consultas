# -*- coding: utf-8 -*-
# Copyright (c) 2020, Lewin Villar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ValidadordeResultados(Document):
	def validate_docs(self):
		if not self.resultados:
			return
		lst = self.resultados.split()
		for r in lst:
			frappe.publish_realtime(
				'validator_progress',
				{"progress": [lst.index(r), len(lst)-1, r]},
				doctype="Validador de Resultados",
				user=frappe.session.user
			)
			if not frappe.db.exists("Resultado", r):
				continue
			res = frappe.get_doc("Resultado", r)
			res.submit()
