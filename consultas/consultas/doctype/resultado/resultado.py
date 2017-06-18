# -*- coding: utf-8 -*-
# Copyright (c) 2017, Lewin Villar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Resultado(Document):
		
	def before_insert(self):
		result = frappe.db.sql("""SELECT CONCAT('RES-',LPAD(current+1,10,0)) as name FROM `tabSeries` WHERE name = 'RES-'""",as_dict=True)
		name = result[0].name
		frappe.msgprint(name)
		consulta = frappe.get_doc(self.consulta_tipo,self.consulta)
		if(consulta):
			consulta.resultado = name
			consulta.save()

   	def get_list_indice_quimicos(self):
		
		paciente=frappe.get_doc("Paciente",self.paciente)
		if(paciente):
			self.edad=paciente.edad
			self.sexo=paciente.sexo
			self.telefono=paciente.telefono if paciente.telefono else "-" 
			self.cedula_pasaporte=paciente.cedula_pasaporte if paciente.cedula_pasaporte else "-"
			self.direccion=paciente.direccion if paciente.direccion else "-"			

		result = frappe.db.sql("""SELECT name as prueba,prueba_nombre,uds,metodo,rango_referencia as rango_ref
		FROM `tabIndice Prueba` 
			WHERE prueba_name IN (select prueba from `viewPruebas En Consulta` WHERE parent='{0}') AND serologia=0"""
			.format(self.consulta),
		as_dict=True)
		
		self.indices_pruebas = []
		for prueba in result:
			self.append("indices_pruebas",prueba)
		
		result = frappe.db.sql("""SELECT name as prueba,prueba_nombre,uds,metodo,rango_referencia as rango_ref
		FROM `tabIndice Prueba` 
			WHERE prueba_name IN (select prueba from `viewPruebas En Consulta` WHERE parent='{0}') AND serologia=1"""
			.format(self.consulta),
		as_dict=True)
		
		self.serologia = []
		for prueba in result:
			self.append("serologia",prueba)
			
		self.indices_hematologicos = []	
		for indice in frappe.get_list("Indice Hematologico", {"disponible": 1,"recuento_diferencial":0}, ["name", "uds","rango_referencia"],order_by="creation ASC", limit_page_length=0):
			
			self.append("indices_hematologicos",{
				"rango_referencia": indice.rango_referencia,
				"uds": indice.uds,
				#"resultado":"-",
				"indice_hematologico":indice.name
			})
		
		self.recuento_diferencial = []	
		for indice in frappe.get_list("Indice Hematologico", {"disponible": 1,"recuento_diferencial":1}, ["name", "uds","rango_referencia"],order_by="creation ASC", limit_page_length=0):
			
			self.append("recuento_diferencial",{	
				"rango_referencia": indice.rango_referencia,
				"uds": indice.uds,
				#"resultado":"-",
				"indice_hematologico":indice.name
			})
			
		self.indices_urinarios = []	
		for indice in frappe.get_list("Indice Urinario", {"disponible": 1,"sedimento_urinario":0},["nombre"],order_by="creation ASC",limit_page_length=0):
		
			self.append("indices_urinarios",{
				"indice_urinario": indice.nombre, 
				#"examen_fisicoquimico":""
				
			})
		self.sedimentos_urinarios = []	
		for indice in frappe.get_list("Indice Urinario", {"disponible": 1,"sedimento_urinario":1},["nombre"],order_by="creation ASC",limit_page_length=0):
		
			self.append("sedimentos_urinarios",{
				"indice_urinario": indice.nombre, 
				#"examen_fisicoquimico":""
				
			})