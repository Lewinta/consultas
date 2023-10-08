	# -*- coding: utf-8 -*-
# Copyright (c) 2017, Lewin Villar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import hashlib
from frappe.model.document import Document
from consultas.consultas.api import get_rango_por_edad

class Resultado(Document):
	def on_submit(self):
		if self.sucursal != "EMP-000020":
			return
		consulta = frappe.get_doc(self.consulta_tipo, self.consulta)
		# Assign Resultado to Consulta
		consulta.resultado = self.name

		if consulta.docstatus == 0:
			consulta.submit()

	def on_cancel(self):
		consulta = frappe.get_doc(self.consulta_tipo, self.consulta)
		if consulta.docstatus == 1:
			consulta.resultado = ""
			consulta.cancel()

	def before_print(self):
		if(self.institucion == "MOVILAB"):
			self.letter_head = "Hoja Timbrada Movilab"

	def get_consult_table(self):
		return "tabConsulta Prueba Privada" if self.consulta_tipo == "Consulta Privada" else "tabConsulta Prueba"

	def refresh_personal_info(self):
		paciente=frappe.get_doc("Paciente",self.paciente)
		if(paciente):
			consulta = frappe.get_doc(self.consulta_tipo, self.consulta)
			nombre_completo = frappe.get_value("Paciente",self.paciente,"nombre_completo")
			self.edad = paciente.edad
			self.sexo = paciente.sexo
			self.telefono = paciente.telefono if paciente.telefono else "-" 
			self.cedula_pasaporte = paciente.cedula_pasaporte if paciente.cedula_pasaporte else "-"
			self.direccion = paciente.direccion if paciente.direccion else "-"			
			self.nombre_completo = nombre_completo			
			if consulta.medico:			
				self.medico = consulta.medico 
			if consulta.institucion:			
				self.institucion = consulta.institucion 

		return True
	# def remove_result_to_consult(self):	
	# 	# Remove Resultado to Consulta Privada
	# 	if not self.consulta:
	# 	    return
	# 	cp = frappe.get_doc(self.consulta_tipo, self.consulta)
	# 	cp.resultado = ""
	# 	cp.db_update()

	# def on_cancel(self):
		# self.remove_result_to_consult()


	# def on_trash(self):
	# 	self.remove_result_to_consult()

	def after_insert(self):
		self.key = self.get_signature()

		self.print_url = "{url}/{doctype}/{name}?key={key}".format(**{
			"url": frappe.utils.get_url(),
			"doctype": self.doctype,
			"name": self.name,
			"key": self.key
		})

		self.db_update()
		
	def before_insert(self):
		result = frappe.db.sql("""SELECT CONCAT('RES-',LPAD(current+1,10,0)) as name FROM `tabSeries` WHERE name = 'RES-'""",as_dict=True)
		name = result[0].name
		consulta = frappe.get_doc(self.consulta_tipo,self.consulta)
		if(consulta):
			consulta.resultado = name
		
	
	def get_quimica(self):

		temp = self.indices_pruebas if hasattr(self,'indices_pruebas') else 0.00 

		result = frappe.db.sql("""SELECT C.prueba AS name, I.prueba_nombre AS prueba, I.uds, I.metodo,I.name as indice,I.rango_por_edad, I.rango_referencia AS rango_ref
			FROM 
				`tabIndice Prueba` I JOIN `{0}` C 
			ON 
				I.prueba = C.prueba 
			WHERE 
				C.parent = '{1}' AND I.grupo = 'QUIMICA' AND C.prueba != 'PRB-000000149'
			ORDER BY C.idx"""
			.format(self.get_consult_table(), self.consulta),
		as_dict=True)
		
		# result = frappe.db.sql("""SELECT prueba as name,prueba_nombre as prueba,uds,metodo,rango_referencia as rango_ref
		# FROM `tabIndice Prueba` 
		# 	WHERE prueba_name IN (select prueba from `{0}` WHERE parent='{0}') AND grupo = 'QUIMICA'"""
		# 	.format(self.consulta),
		# as_dict=True)
		
		self.indices_pruebas = []
		self.test_quimicos = 1 if result else 0
		for prueba in result:
			if (prueba.rango_por_edad):
				prueba.rango_ref = get_rango_por_edad(prueba.indice, self.edad)

			if prueba.name == "PRB-000000149":
				continue
			if prueba.name == "PRB-000000044":
				self.append("indices_pruebas",{"prueba":"BILIRRUBINA TOTAL","metodo":"QLM","rango_ref":"0.0 - 1.00","uds":"MG/DL"})
				self.append("indices_pruebas",{"prueba":"DIRECTA","metodo":"QLM","rango_ref":"0-0.20","uds":"MG/DL"})
				self.append("indices_pruebas",{"prueba":"INDIRECTA","metodo":"QLM","rango_ref":"-","uds":"MG/DL"})
				continue
			if prueba.name == "PRB-000000046":
				self.append("indices_pruebas",{"prueba":"PROTEINAS TOTALES","metodo":"QLM","rango_ref":"6.0 - 8.0","uds":"MG/DL"})
				self.append("indices_pruebas",{"prueba":"ALBUMINA","metodo":"QLM","rango_ref":"3.5 - 4.8","uds":"MG/DL"})
				self.append("indices_pruebas",{"prueba":"GLOBULINA","metodo":"QLM","rango_ref":"2.0 - 4.0","uds":"MG/DL"})
				self.append("indices_pruebas",{"prueba":"INDICE A/G","metodo":"QLM","rango_ref":"1.2 - 2.2","uds":"MG/DL"})
				continue
			if prueba.name == "PRB-000000271":
				self.append("indices_pruebas",{"prueba":"HIERRO TOTAL","metodo":"  ","rango_ref":"50 - 120","uds":"ug/DL"})
				self.append("indices_pruebas",{"prueba":"T I B C","metodo":"  ","rango_ref":"250 - 400","uds":"ug/DL"})
				self.append("indices_pruebas",{"prueba":"% de Saturation","metodo":"  ","rango_ref":"20 - 55","uds":"%"})
				continue
			if prueba.name == "PRB-000000275":
				self.append("indices_pruebas",{"prueba":"GLUCOSA EN AYUNAS","metodo":"QML","rango_ref":"60 - 110","uds":"MG/DL"})
				self.append("indices_pruebas",{"prueba":"GLUCOSA 30 MINUTOS","metodo":"QML","rango_ref":"60 - 110","uds":"MG/DL"})
				self.append("indices_pruebas",{"prueba":"GLUCOSA 60 MINUTOS","metodo":"QML","rango_ref":"60 - 110","uds":"MG/DL"})
				self.append("indices_pruebas",{"prueba":"GLUCOSA 90 MINUTOS","metodo":"QML","rango_ref":"60 - 110","uds":"MG/DL"})
				self.append("indices_pruebas",{"prueba":"GLUCOSA 120 MINUTOS","metodo":"QML","rango_ref":"60 - 110","uds":"MG/DL"})
				continue
			if prueba.name == "PRB-000000338":
				self.append("indices_pruebas",{"prueba":"GLUCOSA BASAL","metodo":" ","rango_ref":"NEG - POS","uds":" "})
				self.append("indices_pruebas",{"prueba":"GLUCOSA 30 MINUTOS","metodo":" ","rango_ref":"NEG - POS","uds":" "})
				self.append("indices_pruebas",{"prueba":"GLUCOSA 60 MINUTOS","metodo":" ","rango_ref":"NEG - POS","uds":" "})
				self.append("indices_pruebas",{"prueba":"GLUCOSA 90 MINUTOS","metodo":" ","rango_ref":"NEG - POS","uds":" "})
				self.append("indices_pruebas",{"prueba":"GLUCOSA 120 MINUTOS","metodo":" ","rango_ref":"NEG - POS","uds":" "})
				continue
			# self.append("indices_pruebas",prueba)
			self.append("indices_pruebas",{"prueba":prueba.prueba,"metodo":prueba.metodo,"rango_ref":prueba.rango_ref,"uds":prueba.uds})
		if temp and result:
			for row in self.indices_pruebas:
				for tmp in temp:
					if row.prueba == tmp.prueba:
						row.resultado = tmp.resultado
		return True

	def get_serologia(self):
		temp = self.serologia  if hasattr(self,'serologia') else 0.00 
		result = frappe.db.sql("""SELECT C.prueba AS prueba_cod, I.prueba_nombre AS prueba, I.uds, I.metodo, I.rango_referencia AS rango_ref
			FROM 
				`tabIndice Prueba` I JOIN `{0}` C 
			ON 
				I.prueba = C.prueba 
			WHERE 
				C.parent = '{1}' AND I.grupo = 'SEROLOGIA'
			ORDER BY C.idx"""
			.format(self.get_consult_table(), self.consulta),
		as_dict=True)
		
		self.serologia = []
		self.test_serologia = 1 if result else 0
		for prueba in result:
			self.append("serologia", prueba)
			if prueba.prueba_cod == "PRB-000000314":
				self.append("serologia",{"prueba":"SALMONELLA TYPHI O","metodo":"-","rango_ref":"NEG - POS","uds":"-"})
				self.append("serologia",{"prueba":"SALMONELLA TYPHI H","metodo":"-","rango_ref":"NEG - POS","uds":"-"})
				self.append("serologia",{"prueba":"PARATYPHI B(O)","metodo":"-","rango_ref":"NEG - POS","uds":"-"})
				self.append("serologia",{"prueba":"PARATYPHI B(H)","metodo":"-","rango_ref":"NEG - POS","uds":"-"})
				self.append("serologia",{"prueba":"BRUCELLAS ABORTUS","metodo":"-","rango_ref":"NEG - POS","uds":"-"})
				self.append("serologia",{"prueba":"PROTEUS O-X-19","metodo":"-","rango_ref":"NEG - POS","uds":"-"})

				continue
			if prueba.prueba_cod == "PRB-000000317":
				self.append("serologia",{"prueba":"ACS IGG ANTI SARS-COV-2","metodo":"INMUNOCROMATOGRAFIA CUALITATIVA","rango_ref":"NEG - POS","uds":"-"})
				self.append("serologia",{"prueba":"ACS IGM ANTI SARS-COV-2","metodo":"INMUNOCROMATOGRAFIA CUALITATIVA","rango_ref":"NEG - POS","uds":"-"})

				continue
			if prueba.prueba_cod == "PRB-000000344":
				self.append("serologia",{"prueba":"ACS IGM ANTI SARS-COV-2","metodo":"INMUNOCROMATOGRAFIA CUANTITATIVA","rango_ref":"0.0 - 0.04","uds":"-"})
				self.append("serologia",{"prueba":"ACS IGG ANTI SARS-COV-2","metodo":"INMUNOCROMATOGRAFIA CUANTITATIVA","rango_ref":"0.0 - 0.04","uds":"-"})

				continue

		if temp and result:
			for row in self.serologia:
				for tmp in temp:
					if row.prueba == tmp.prueba:
						row.resultado = tmp.resultado
		return True

	def get_inmunodiagnostico(self):
		temp = self.inmunodiagnosticos if hasattr(self,'inmunodiagnosticos') else 0.00 
		result = frappe.db.sql("""
			SELECT 
				C.prueba AS name, I.prueba_nombre AS prueba, I.uds, I.metodo, I.rango_referencia AS rango_ref
			FROM 
				`tabIndice Prueba` I 
			JOIN 
				`{0}` C 
			ON 
				I.prueba = C.prueba 
			WHERE 
				C.parent = '{1}' AND I.grupo = 'INMUNODIAGNOSTICOS'
			AND 
				C.prueba <>'PRB-000000224'
			ORDER BY 
				C.idx
			"""
			.format(self.get_consult_table(), self.consulta),
		as_dict=True)
		
		self.inmunodiagnosticos = []
		self.test_inmunodiagnosticos = 1 if result else 0 
		for prueba in result:
			if prueba.name == "PRB-000000270":
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba": "CHLAMYDIA TRACHOMATIS", "metodo": " ", "rango_ref": " ", "uds": "ANEXOS"})	
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba": "NEISSERIA GONORRHOEAE", "metodo": " ", "rango_ref": " " , "uds": "ANEXOS"})	
				continue 

			if prueba.name == "PRB-000000048":
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"PSA TOTAL", "metodo": "QLM", "rango_ref": "0 - 4.0", "uds": "ng/ml"})	
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"PSA LIBRE", "metodo": "QLM", "rango_ref": "-", "uds": "ng/ml"})	
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"% PSA LIBRE/PSA TOTAL", "metodo": "QLM", "rango_ref": "> 11.0", "uds": "ng/ml"})	
				continue 

			if prueba.name == "PRB-000000059":
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba": "TIEMPO DE PROTOMBINA (PT) +  INR", "metodo": "-", "rango_ref": "11 - 17", "uds": "SEGUNDOS"})	
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba": " ", "metodo": "CONTROL", "rango_ref": "          ", "uds": "SEGUNDOS"})	
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba": " ", "metodo": "INR"    , "rango_ref": "0.9 - 1.2" , "uds": "SEGUNDOS"})	
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba": " ", "metodo": "%"      , "rango_ref": "70 - 120"," uds":"%"})	
				continue

			if prueba.name == "PRB-000000352":
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba": "INFLUENZA A", "metodo": " ", "rango_ref": "NEG - POS", "uds": " "})	
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba": "INFLUENZA B", "metodo": " "    , "rango_ref": "NEG - POS" , "uds": " "})	
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba": "INFLUENZA H1N1", "metodo": " "  , "rango_ref": "NEG - POS"," uds":" "})	
				continue

			if prueba.name == "PRB-000000060":
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"TIEMPO DE TROMBOPLASTINA PARCIAL (PTT)", "metodo": "-", "rango_ref": "22 - 30", "uds": "SEGUNDOS"})
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":" ", "metodo": "CONTROL", "rango_ref": "          ", "uds": "SEGUNDOS"})
				continue

			if prueba.name == "PRB-000000095":
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"SALMONELLA TYPHI O", "metodo": " ", "rango_ref": "          ", "uds": " "})	
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"SALMONELLA TYPHI H", "metodo": " ", "rango_ref": "          ", "uds": " "})	
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"PARATYPHI B(O)", "metodo": " ", "rango_ref": "          ", "uds": " "})	
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"PARATYPHI B(H)", "metodo": " ", "rango_ref": "          ", "uds": " "})	
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"BRUCELLAS ABORTUS", "metodo": " ", "rango_ref": "          ", "uds": " "})	
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"PROTEUS O-X-19", "metodo": " ", "rango_ref": "          ", "uds": " "})
				continue 

			if prueba.name == "PRB-000000287":
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"HEPATITIS C RNA", "metodo": " ", "rango_ref": "ANEXOS", "uds": "UI/mL"})	
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"HEPATITIS C RNA", "metodo": " ", "rango_ref": "ANEXOS", "uds": "Log10"})	
				self.test_prb_000000287 = 1
				self.test_anexos==1
				continue 

			if prueba.name == "PRB-000000299":
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"ANA", "metodo": "IFI", "rango_ref": "  ", "uds": "  "})	
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"HISTONA", "metodo": "CLIA", "rango_ref": "ANEXOS", "uds": "INDICE"})	
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"RO52", "metodo": "CLIA", "rango_ref": "          ", "uds": " "})	
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"RO60", "metodo": "CLIA", "rango_ref": "          ", "uds": " "})	
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"SS-B", "metodo": "CLIA", "rango_ref": "          ", "uds": " "})	
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"SM", "metodo": "CLIA", "rango_ref": "          ", "uds": " "})
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"RNP", "metodo": "CLIA", "rango_ref": "          ", "uds": " "})
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"SCL-70", "metodo": "CLIA", "rango_ref": "          ", "uds": " "})
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"JO-1", "metodo": "CLIA", "rango_ref": "          ", "uds": " "})
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"CENTROMERO", "metodo": "CLIA", "rango_ref": "          ", "uds": " "})
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"RIBOSOMAL P", "metodo": "CLIA", "rango_ref": "          ", "uds": " "})
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"dsDNA", "metodo": "CLIA", "rango_ref": "ANEXOS", "uds": "UI/mL"})
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"ANTI-TPO", "metodo": "ECLIA", "rango_ref": "9 -  34", "uds": "UI/mL"})
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"C3", "metodo": "INMUNOTURBID.", "rango_ref": "90 - 180", "uds": "mg/dL"})
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"C4", "metodo": "INMUNOTURBID.", "rango_ref": "10 - 40", "uds": "mg/dL"})
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba":"FACTOR REUMATOIDE", "metodo": "INMUNOTURBID.", "rango_ref": "< 14.0", "uds": "UI/mL"})
				continue 
			
			if prueba.name == "PRB-000000368":
				self.test_otros_cultivos = 1
				continue

			if prueba.name == "PRB-000000322":
				self.append("inmunodiagnosticos", {"prueba_name": prueba.prueba_name, "prueba": "CD4, CD8, CD3, COOPERADOR/SUPRESOR", "metodo": " ", "rango_ref": "      ", "uds": " "})
				self.append("inmunodiagnosticos", {"prueba_name": prueba.prueba_name, "prueba": "CONTEO TOTAL LEUCOCITOS", "metodo": " ", "rango_ref": "      ", "uds": " "})
				self.append("inmunodiagnosticos", {"prueba_name": prueba.prueba_name, "prueba": "CONTEO TOTAL LINFOCITOS", "metodo": " ", "rango_ref": "      ", "uds": " "})
				self.append("inmunodiagnosticos", {"prueba_name": prueba.prueba_name, "prueba": "% DE LINFOCITOS", "metodo": " ", "rango_ref": "      ", "uds": " "})
				self.append("inmunodiagnosticos", {"prueba_name": prueba.prueba_name, "prueba": "CONTEO ABSOLUTO CD4", "metodo": " ", "rango_ref": "       ", "uds": " "})
				self.append("inmunodiagnosticos", {"prueba_name": prueba.prueba_name, "prueba": "CONTEO ABSOLUTO CD8", "metodo": " ", "rango_ref": "      ", "uds": " "})
				self.append("inmunodiagnosticos", {"prueba_name": prueba.prueba_name, "prueba": "CONTEO ABSOLUTO CD3", "metodo": " ", "rango_ref": "      ", "uds": " "})
				self.append("inmunodiagnosticos", {"prueba_name": prueba.prueba_name, "prueba": "RELACION CD4/CD8", "metodo": " ", "rango_ref": "      ", "uds": " "})
				self.append("inmunodiagnosticos", {"prueba_name": prueba.prueba_name, "prueba": "RELACION CD4/CD3", "metodo": " ", "rango_ref": "      ", "uds": " "})
				self.append("inmunodiagnosticos", {"prueba_name": prueba.prueba_name, "prueba": "RELACION CD8/CD3", "metodo": " ", "rango_ref": "      ", "uds": " "})
				continue

			if prueba.name == "PRB-000000386":
				self.append("inmunodiagnosticos", {"prueba_name": prueba.prueba_name, "prueba": "ATUN", "metodo": "InmunoCAP", "rango_ref": "< 0.10", "uds": "kU/L"})
				self.append("inmunodiagnosticos", {"prueba_name": prueba.prueba_name, "prueba": "BACALAO", "metodo": "InmunoCAP", "rango_ref": "< 0.10", "uds": "kU/L"})
				self.append("inmunodiagnosticos", {"prueba_name": prueba.prueba_name, "prueba": "CAMARONES", "metodo": "InmunoCAP", "rango_ref": "< 0.10", "uds": "kU/L"})
				self.append("inmunodiagnosticos", {"prueba_name": prueba.prueba_name, "prueba": "CANGREJO", "metodo": "InmunoCAP", "rango_ref": "< 0.10", "uds": "kU/L"})
				self.append("inmunodiagnosticos", {"prueba_name": prueba.prueba_name, "prueba": "LANGOSTA", "metodo": "InmunoCAP", "rango_ref": "< 0.10", "uds": "kU/L"})
				self.append("inmunodiagnosticos", {"prueba_name": prueba.prueba_name, "prueba": "MEJILLON", "metodo": "InmunoCAP", "rango_ref": "< 0.10", "uds": "kU/L"})
				self.append("inmunodiagnosticos", {"prueba_name": prueba.prueba_name, "prueba": "PULPO", "metodo": "InmunoCAP", "rango_ref": "< 0.10", "uds": "kU/L"})
				self.append("inmunodiagnosticos", {"prueba_name": prueba.prueba_name, "prueba": "SALMON", "metodo": "InmunoCAP", "rango_ref": "< 0.10", "uds": "kU/L"})
				self.test_prb_000000386 = 1
				self.test_anexos==1
				continue
			
			self.append("inmunodiagnosticos",{"prueba":prueba.prueba,"metodo":prueba.metodo,"rango_ref":prueba.rango_ref,"uds":prueba.uds})

			if temp:
				for row in self.inmunodiagnosticos:
					for tmp in temp:
						if row.prueba == tmp.prueba:
							row.resultado = tmp.resultado

	def get_espermatograma(self):
		temp_examen_macroscopico = self.examen_macroscopico if hasattr(self,'examen_macroscopico') else 0.00 
		temp_examen_microscopico = self.examen_microscopico if hasattr(self,'examen_microscopico') else 0.00 
		temp_evaluacion_mortalidad = self.evaluacion_mortalidad if hasattr(self,'evaluacion_mortalidad') else 0.00 
		temp_concentracion = self.concentracion if hasattr(self,'concentracion') else 0.00 
		temp_morfologia_espermatica = self.morfologia_espermatica if hasattr(self,'morfologia_espermatica') else 0.00 
		result = frappe.db.sql("""SELECT prueba  from `{0}` WHERE parent='{1}' AND prueba  = 'PRB-000000268'"""
			.format(self.get_consult_table(), self.consulta), as_dict=True)
		
		self.examen_macroscopico = []
		self.examen_microscopico = []
		self.evaluacion_mortalidad = []
		self.concentracion = []
		self.morfologia_espermatica = []
		self.test_espermatograma = 1 if result else 0
		

		self.append("examen_macroscopico",{"descripcion": "TIEMPO DE LICUEFACCIÓN", "rango_ref":"< 60 MIN ", "resultado":"", "uds": "MINUTOS"})
		self.append("examen_macroscopico",{"descripcion": "ASPECTO", "rango_ref":"Hom/Opa", "resultado":"", "uds": "-"})
		self.append("examen_macroscopico",{"descripcion": "COLOR", "rango_ref":"GRIS OPALESCENTE", "resultado":"", "uds": "-"})
		self.append("examen_macroscopico",{"descripcion": "VOLUMEN", "rango_ref":">= 2 mL", "resultado":"", "uds": "ML"})
		self.append("examen_macroscopico",{"descripcion": "VISCOSIDAD", "rango_ref":"Normal Fil < 2cm", "resultado":"", "uds": ""})
		self.append("examen_macroscopico",{"descripcion": "PH", "rango_ref":"> 7.2", "resultado":"", "uds": ""})

		self.append("examen_microscopico",{"descripcion": "GLOBULOS BLANCOS", "rango_ref":"-", "resultado":"", "uds": "/CAMPO"})
		self.append("examen_microscopico",{"descripcion": "GLOBULOS ROJOS", "rango_ref":"-", "resultado":"", "uds": "/CAMPO"})
		self.append("examen_microscopico",{"descripcion": "CELULAS EPITELIALES", "rango_ref":"-", "resultado":"", "uds": "/CAMPO"})
		self.append("examen_microscopico",{"descripcion": "CELULAS GERMINALES INMADURAS", "rango_ref":"-", "resultado":"", "uds": "/CAMPO"})
		self.append("examen_microscopico",{"descripcion": "LEVADURAS", "rango_ref":"-", "resultado":"", "uds": " "})
		self.append("examen_microscopico",{"descripcion": "TRICHOMONAS", "rango_ref":"-", "resultado":"", "uds": " "})
		self.append("examen_microscopico",{"descripcion": "BACTERIAS", "rango_ref":"-", "resultado":"", "uds": " "})
		self.append("examen_microscopico",{"descripcion": "AGLUTINACION", "rango_ref":"-", "resultado":"", "uds": " "})

		self.append("evaluacion_mortalidad",{"descripcion": "A) PROGRESIVA RAPIDA", "rango_ref":"-", "resultado":"", "uds": "%"})
		self.append("evaluacion_mortalidad",{"descripcion": "B) PROGRESIVA LENTA", "rango_ref":"-", "resultado":"", "uds": "%"})
		self.append("evaluacion_mortalidad",{"descripcion": "C) NO PROGRESIVA", "rango_ref":"-", "resultado":"", "uds": "%"})
		self.append("evaluacion_mortalidad",{"descripcion": "D) INMOVILES", "rango_ref":"-", "resultado":"", "uds": "%"})
		self.append("evaluacion_mortalidad",{"descripcion": "ESPERMATOZOIDES MOVILES: A+B+C", "rango_ref":"-", "resultado":"", "uds": "%"})
		self.append("evaluacion_mortalidad",{"descripcion": "ESPERMATOZOIDES PROGRESIVOS: A+B", "rango_ref":"> 50%", "resultado":"", "uds": "%"})
		self.append("evaluacion_mortalidad",{"descripcion": "ESPERMATOZOIDES VIVOS", "rango_ref":"> 50%", "resultado":"", "uds": "%"})

		self.append("concentracion",{"descripcion": "ESPERMATOZOIDES/mL", "rango_ref":"-", "resultado":"", "uds": "Mill/mL"})
		self.append("concentracion",{"descripcion": "ESPERMATOZOIDES/eyaculados", "rango_ref":"-", "resultado":"", "uds": "Mill/mL"})

		self.append("morfologia_espermatica",{"descripcion": "NORMALES", "rango_ref":"-", "resultado":"", "uds": "%"})
		self.append("morfologia_espermatica",{"descripcion": "ANORMALES", "rango_ref":"-", "resultado":"", "uds": "%"})
		self.append("morfologia_espermatica",{"descripcion": "DEFECTOS DE CABEZA", "rango_ref":"-", "resultado":"", "uds": "%"})
		self.append("morfologia_espermatica",{"descripcion": "DEFECTOS DE CUELLO Y PIEZA MEDIA", "rango_ref":"-", "resultado":"", "uds": "%"})
		self.append("morfologia_espermatica",{"descripcion": "DEFECTOS DE COLA", "rango_ref":"-", "resultado":"", "uds": "%"})
		self.append("morfologia_espermatica",{"descripcion": "DEFECTOS DE COLA CITOPLASMÁTICA", "rango_ref":"-", "resultado":"", "uds": "%"})

		if temp_examen_macroscopico and result:
			for row in self.examen_macroscopico:
				for tmp in temp_examen_macroscopico:
					if row.descripcion == tmp.descripcion:
						row.resultado = tmp.resultado

		if temp_examen_microscopico and result:
			for row in self.examen_microscopico:
				for tmp in temp_examen_microscopico:
					if row.descripcion == tmp.descripcion:
						row.resultado = tmp.resultado

		if temp_evaluacion_mortalidad and result:
			for row in self.evaluacion_mortalidad:
				for tmp in temp_evaluacion_mortalidad:
					if row.descripcion == tmp.descripcion:
						row.resultado = tmp.resultado

		if temp_concentracion and result:
			for row in self.concentracion:
				for tmp in temp_concentracion:
					if row.descripcion == tmp.descripcion:
						row.resultado = tmp.resultado

		if temp_morfologia_espermatica and result:
			for row in self.morfologia_espermatica:
				for tmp in temp_morfologia_espermatica:
					if row.descripcion == tmp.descripcion:
						row.resultado = tmp.resultado

		return True 
		
	def get_microbiologia(self):
		temp = self.antibiogramas if hasattr(self,'antibiogramas') else 0.00 
		temp1 = self.bacteriologia_vaginal if hasattr(self,'bacteriologia_vaginal') else 0.00 
		result = frappe.db.sql("""SELECT C.prueba AS name, I.prueba_nombre AS prueba, I.uds, I.metodo, I.rango_referencia AS rango_ref
			FROM 
				`tabIndice Prueba` I JOIN `{0}` C 
			ON 
				I.prueba = C.prueba 
			WHERE 
				C.parent = '{1}' AND I.grupo  = 'MICROBIOLOGIA'
			ORDER BY C.idx"""
			.format(self.get_consult_table(), self.consulta), as_dict=True)

		self.antibiogramas = []
		self.test_microbiologia = 1 if result else 0 
		for prueba in result:
			if prueba.name == "PRB-000000184":
				self.test_baciloscopia = 1			

			if prueba.name == "PRB-000000188":
				self.tipo_cultivo = "SECRECION DE OIDO IZQUIERDO"

			if prueba.name == "PRB-000000260":
				self.tipo_cultivo = "SECRECION DE OIDO DERECHO"

			if prueba.name == "PRB-000000191":
				self.tipo_cultivo = "SECRECION URETRAL"

			if prueba.name == "PRB-000000187":
				self.tipo_cultivo = "SECRECION FORUNCULOS"

			if prueba.name == "PRB-000000261":
				self.tipo_cultivo = "ESPUTO"
				self.tipo_microbiologia = "BACILOSCOPIA"

			if prueba.name == "PRB-000000192":
				self.tipo_cultivo = "MATERIA FECAL"

			if prueba.name == "PRB-000000267":
				self.tipo_cultivo = "SEMEN"
				return 0

			if prueba.name == "PRB-000000347":
				self.tipo_cultivo = "HEMOCULTIVO"

			if prueba.name == "PRB-000000194":
				self.tipo_cultivo = "SECRECION DE OIDO"
				
			if prueba.name == "PRB-000000189":
				self.append("bacteriologia_vaginal", {"valor": "BACTERIAS", "resultado": "", "interpretacion": "-"})	
				self.append("bacteriologia_vaginal", {"valor": "CELULAS EPITELIALES", "resultado": "", "interpretacion": "-" })	
				self.append("bacteriologia_vaginal", {"valor": "LEUCOCITOS", "resultado": "", "interpretacion": "-" })	
				self.append("bacteriologia_vaginal", {"valor": "LEVADURAS", "resultado": "", "interpretacion": "-" })	
				self.append("bacteriologia_vaginal", {"valor": "TRICHOMONAS", "resultado": "", "interpretacion": "-" })
				self.tipo_cultivo = "SECRECION VAGINAL"

			# self.append("antibiogramas", {"valor": "CIPROFLOXACIN", "resultado": "", "interpretacion": "-"})	
			# self.append("antibiogramas", {"valor": "BENZILPENCILLINS", "resultado": "", "interpretacion": "-" })	
			# self.append("antibiogramas", {"valor": "CLINDAMYCIN", "resultado": "", "interpretacion": "-" })	
			# self.append("antibiogramas", {"valor": "ERITROMICIN", "resultado": "", "interpretacion": "-" })	
			# self.append("antibiogramas", {"valor": "GENTAMICIN", "resultado": "", "interpretacion": "-" })
			# self.append("antibiogramas", {"valor": "LEVOFLOXACIN", "resultado": "", "interpretacion": "-" })
			# self.append("antibiogramas", {"valor": "LINEZOLID", "resultado": "", "interpretacion": "-" })
			# self.append("antibiogramas", {"valor": "MOXIFLOXACIN", "resultado": "", "interpretacion": "-" })
			# self.append("antibiogramas", {"valor": "NITROFURANTOIN", "resultado": "", "interpretacion": "-" })
			# self.append("antibiogramas", {"valor": "QUINUPRI/DALFOPRI", "resultado": "", "interpretacion": "-" })
			# self.append("antibiogramas", {"valor": "RIFAMPICIN", "resultado": "", "interpretacion": "-" })
			# self.append("antibiogramas", {"valor": "T. SULFA", "resultado": "", "interpretacion": "-" })
			# self.append("antibiogramas", {"valor": "TETRACYCLINE", "resultado": "", "interpretacion": "-" })
			# self.append("antibiogramas", {"valor": "TIGECICLINAS", "resultado": "", "interpretacion": "-" })
			# self.append("antibiogramas", {"valor": "VACOMYCIN", "resultado": "", "interpretacion": "-" })
			# self.append("antibiogramas", {"valor": "CEFOXITIN", "resultado": "", "interpretacion": "-" })

			# self.append("antibiogramas", {"valor": "AMIKACIN", "resultado": "", "interpretacion": "-"})
			# self.append("antibiogramas", {"valor": "AMPILICIN", "resultado": "", "interpretacion": "-"})
			# self.append("antibiogramas", {"valor": "CEFAZOLIN", "resultado": "", "interpretacion": "-"})
			# self.append("antibiogramas", {"valor": "CEFEPIME", "resultado": "", "interpretacion": "-"})
			# self.append("antibiogramas", {"valor": "CEFTAZIDIME", "resultado": "", "interpretacion": "-"})
			# self.append("antibiogramas", {"valor": "CIPROFLOXACIN", "resultado": "", "interpretacion": "-"})
			# self.append("antibiogramas", {"valor": "CEFTRIAXONE", "resultado": "", "interpretacion": "-"})
			# self.append("antibiogramas", {"valor": "GENTAMICIN", "resultado": "", "interpretacion": "-"})
			# self.append("antibiogramas", {"valor": "IMIPENEM", "resultado": "", "interpretacion": "-"})
			# self.append("antibiogramas", {"valor": "NITROFURANTOIN", "resultado": "", "interpretacion": "-"})
			# self.append("antibiogramas", {"valor": "LEVOFLOXACIN", "resultado": "", "interpretacion": "-"})
			# self.append("antibiogramas", {"valor": "POPERAC", "resultado": "", "interpretacion": "-"})
			# self.append("antibiogramas", {"valor": "TOBRAMYCIN", "resultado": "", "interpretacion": "-"})
			# self.append("antibiogramas", {"valor": "TRIMETHO", "resultado": "", "interpretacion": "-"})
			# self.append("antibiogramas", {"valor": "ERTAPENEM", "resultado": "", "interpretacion": "-"})

			self.append("antibiogramas", {"valor": "AC. NALIDIXICO", "resultado": "", "interpretacion": "-"})
			self.append("antibiogramas", {"valor": "AMIKACINA", "resultado": "", "interpretacion": "-"})
			self.append("antibiogramas", {"valor": "AMOXICILINA", "resultado": "", "interpretacion": "-"})
			self.append("antibiogramas", {"valor": "AMOXICILINA /AC. CLAVULÂNICO", "resultado": "", "interpretacion": "-"})
			self.append("antibiogramas", {"valor": "AMPICILINA", "resultado": "", "interpretacion": "-"})
			self.append("antibiogramas", {"valor": "CEFOTAXIMA", "resultado": "", "interpretacion": "-"})
			self.append("antibiogramas", {"valor": "CEFTAZIDIME", "resultado": "", "interpretacion": "-"})
			self.append("antibiogramas", {"valor": "CIPROFIOXACINA", "resultado": "", "interpretacion": "-"})
			self.append("antibiogramas", {"valor": "FOSFOMICINA", "resultado": "", "interpretacion": "-"})
			self.append("antibiogramas", {"valor": "GENTAMICINA", "resultado": "", "interpretacion": "-"})
			self.append("antibiogramas", {"valor": "IMIPENEM", "resultado": "", "interpretacion": "-"})
			self.append("antibiogramas", {"valor": "LEVOFLOXACINA", "resultado": "", "interpretacion": "-"})
			self.append("antibiogramas", {"valor": "NORFLOXACINA", "resultado": "", "interpretacion": "-"})
			self.append("antibiogramas", {"valor": "OFLOXACINA", "resultado": "", "interpretacion": "-"})
			self.append("antibiogramas", {"valor": "SULFAMETOXAZOLE/TRIMETROPINA", "resultado": "", "interpretacion": "-"})


		if temp and result:
			for row in self.antibiogramas:
				for tmp in temp:
					if row.valor == tmp.valor :
						row.resultado = tmp.resultado
						row.interpretacion = tmp.interpretacion

		if temp1 and result:
			for row in self.bacteriologia_vaginal:
				for tmp in temp:
					if row.valor == tmp.valor :
						row.resultado = tmp.resultado
						row.interpretacion = tmp.interpretacion
		

		return True
	
	def get_hormonas(self):
		temp = self.hormonas if hasattr(self,'hormonas') else 0.00 
		result = frappe.db.sql("""SELECT I.prueba_nombre AS prueba, I.uds, I.metodo, I.rango_referencia AS rango_ref
			FROM 
				`tabIndice Prueba` I JOIN `{0}` C 
			ON 
				I.prueba = C.prueba 
			WHERE 
				C.parent = '{1}' AND I.grupo  = 'HORMONAS'
			ORDER BY C.idx"""
			.format(self.get_consult_table(), self.consulta),
		as_dict=True)
		
		self.hormonas = []
		self.test_hormonas = 1 if result else  0 
		for prueba in result:
			self.append("hormonas",prueba)
		if temp and result:
			for row in self.hormonas:
				for tmp in temp:
					if row.prueba == tmp.prueba:
						row.resultado = tmp.resultado
		return True

	def get_tipificacion(self):
		temp = self.tipificacion if hasattr(self,'tipificacion') else 0.00 
		result = frappe.db.sql("""SELECT C.prueba AS name, I.prueba_nombre AS prueba, I.uds, I.metodo, I.rango_referencia AS rango_ref
			FROM 
				`tabIndice Prueba` I JOIN `{0}` C 
			ON 
				I.prueba = C.prueba 
			WHERE 
				C.parent = '{1}' AND I.grupo = 'INMUNODIAGNOSTICOS' AND C.prueba = 'PRB-000000224' """  
			.format(self.get_consult_table(), self.consulta),
		as_dict=True)
		
		self.tipificacion = []
		self.test_tipificacion = 1 if result else 0 
		if self.test_tipificacion:
			self.test_inmunodiagnosticos = 1

		for prueba in result:
			self.append("tipificacion",prueba)
		if temp and result:
			for row in self.tipificacion:
				for tmp in temp:
					if row.prueba == tmp.prueba:
						row.resultado = tmp.resultado
		return True

	def get_hematologia(self):
		def compare_lists(l1, l2):
			for itm in l1:
				if itm in l2:
					return True
			return False
		temp = self.indices_hematologicos if hasattr(self,'indices_hematologicos') else 0.00 
		result = frappe.db.sql("""SELECT prueba from `{0}` WHERE parent='{1}' AND prueba in ('PRB-000000195', 'PRB-000000310', 'PRB-000000205', 'PRB-000000207', 'PRB-000000198', 'PRB-000000374') """  
			.format(self.get_consult_table(), self.consulta), as_dict=True)
		result = [n.prueba for n in result]

		self.indices_hematologicos = []
		self.test_hematologico = 1 if 'PRB-000000195' in result else 0
		self.test_extendido_periferico = 1 if 'PRB-000000374' in result else 0
		self.test_otros_hematologico = 1 if compare_lists(['PRB-000000310', 'PRB-000000205', 'PRB-000000198', 'PRB-000000207', 'PRB-000000374'], result)  else 0
		frappe.errprint(result)
		if 'PRB-000000195' in result:
			for indice in frappe.get_list("Indice Hematologico", {"disponible": 1,"recuento_diferencial":0,"otros_hematologia":0}, ["name", "uds","rango_referencia"],order_by="creation ASC", limit_page_length=0):
				
				self.append("indices_hematologicos",{
					"rango_referencia": indice.rango_referencia,
					"uds": indice.uds,
					#"resultado":"-",
					"indice_hematologico":indice.name
				})

			if temp and result:
				for row in self.indices_hematologicos:
					for tmp in temp:
						if row.indice_hematologico == tmp.indice_hematologico:
							row.resultado = tmp.resultado
		
		temp = self.recuento_diferencial if hasattr(self,'recuento_diferencial') else 0.00 
		self.recuento_diferencial = []	
		
		if 'PRB-000000195' in result:
			for indice in frappe.get_list("Indice Hematologico", {"disponible": 1,"recuento_diferencial":1}, ["name", "uds","rango_referencia"],order_by="creation ASC", limit_page_length=0):
				
				self.append("recuento_diferencial",{	
					"rango_referencia": indice.rango_referencia,
					"uds": indice.uds,
					#"resultado":"-",
					"indice_hematologico":indice.name
				})

			if temp and result:
				for row in self.recuento_diferencial:
					for tmp in temp:
						if row.indice_hematologico == tmp.indice_hematologico:
							row.resultado = tmp.resultado

		self.otros_hematologia = []
			
		if compare_lists(['PRB-000000310', 'PRB-000000205', 'PRB-000000198', 'PRB-000000207'], result):
			# frappe.errprint("Contine otros_hematologia")
			consulta = frappe.get_doc( self.consulta_tipo, self.consulta )	
			
			for p in consulta.pruebas:
				for indice in  frappe.get_list("Indice Hematologico",{"prueba":p.prueba},["indice_hematologico","rango_referencia","uds"]):
					self.append("otros_hematologia",indice)

		return True

	def get_urianalisis(self):

		self.test_urianalisis = 1 if self.has_urianalisis() else 0

		temp = self.indices_urinarios if hasattr(self,'indices_urinarios') else 0.00 
		self.indices_urinarios = []
		result = frappe.get_list("Indice Urinario", {"disponible": 1,"sedimento_urinario":0,"coprologico":0},["nombre"],order_by="creation ASC",limit_page_length=0)
		for indice in result:
			self.append("indices_urinarios",{
				"indice_urinario": indice.nombre, 
				#"examen_fisicoquimico":""
				
			})

		if temp and result:
			for row in self.indices_urinarios:
				for tmp in temp:
					if row.indice_urinario == tmp.indice_urinario:
						row.examen_fisicoquimico = tmp.examen_fisicoquimico

		temp = self.sedimentos_urinarios if hasattr(self,'sedimentos_urinarios') else 0.00 

		self.sedimentos_urinarios = []	
		result = frappe.get_list("Indice Urinario", {"disponible": 1,"sedimento_urinario":1, "coprologico":0},["nombre"],order_by="creation ASC",limit_page_length=0)
		for indice in result:
			self.append("sedimentos_urinarios",{
				"indice_urinario": indice.nombre, 
				#"examen_fisicoquimico":""
				
			})

		if temp and result:
			for row in self.sedimentos_urinarios:
				for tmp in temp:
					if row.indice_urinario == tmp.indice_urinario:
						row.examen_fisicoquimico = tmp.examen_fisicoquimico
		return True
	
	def get_otros_uroanalisis(self):
		temp = self.otros_uroanalisis  if hasattr(self,'otros_uroanalisis') else 0.00 
		result = frappe.db.sql("""SELECT C.prueba AS prueba_cod, I.prueba_nombre AS prueba, I.uds, I.metodo, I.rango_referencia AS rango_ref
			FROM 
				`tabIndice Prueba` I JOIN `{0}` C 
			ON 
				I.prueba = C.prueba 
			WHERE 
				C.parent = '{1}' AND I.grupo = 'OTROS UROANALISIS'
			ORDER BY C.idx"""
			.format(self.get_consult_table(), self.consulta), as_dict=True)
		
		self.otros_uroanalisis = []
		self.test_otros_uroanalisis = 1 if result else 0
		for prueba in result:
			# self.append("otros_uroanalisis", prueba)
			if prueba.prueba_cod == "PRB-000000353":
				self.append("otros_uroanalisis",{"prueba":"CRENADOS","metodo":"-","rango_ref":"0 - 100","uds":"%"})
				self.append("otros_uroanalisis",{"prueba":"DISFORMICOS","metodo":"-","rango_ref":"0 - 100","uds":"%"})
				self.append("otros_uroanalisis",{"prueba":"NORMALES","metodo":"-","rango_ref":"0 - 100","uds":"%"})
				self.append("otros_uroanalisis",{"prueba":"TOTAL GLOBULOS OBSERVADOS","metodo":"-","rango_ref":" ","uds":"p/c"})
				self.append("otros_uroanalisis",{"prueba":"SANGRE OCULTA","metodo":"-","rango_ref":"NEG - POS","uds":" "})

				continue

		if temp and result:
			for row in self.otros_uroanalisis:
				for tmp in temp:
					if row.prueba == tmp.prueba:
						row.resultado = tmp.resultado
		return True

	def get_coprologia(self):
		temp = self.aspecto_fisico if hasattr(self,'aspecto_fisico') else 0.00 
		self.aspecto_fisico = []
		filters = {"disponible": 1, "coprologico":1, "tipo_indice":"Aspecto Fisico"}
		result = frappe.get_list("Indice Urinario", filters,["nombre"],order_by="creation ASC",limit_page_length=0)
		tiene_copro = frappe.db.sql("""SELECT prueba from `{0}` WHERE parent='{1}' AND prueba = 'PRB-000000144' """  
			.format(self.get_consult_table(), self.consulta), as_dict=True)
		 
		self.test_coprologico = 1 if result and tiene_copro else 0	
		for indice in result:
		
			self.append("aspecto_fisico",{
				"indice_urinario": indice.nombre, 
				#"examen_fisicoquimico":""
				
			})

		if temp and result:
			for row in self.aspecto_fisico:
				for tmp in temp:
					if row.indice_urinario == tmp.indice_urinario:
						row.examen_fisicoquimico = tmp.examen_fisicoquimico

		temp = self.aspecto_microscopico  if hasattr(self,'aspecto_microscopico') else 0.00 
		self.aspecto_microscopico = []	
		filters = {"disponible": 1, "coprologico":1, "tipo_indice":"Aspecto Microscopico"}
		result = frappe.get_list("Indice Urinario", filters, ["nombre"], order_by="nombre ASC")
		for indice in result:
			frappe.errprint(indice.nombre)
			self.append("aspecto_microscopico",{
				"indice_urinario": indice.nombre, 
				#"examen_fisicoquimico":""
				
			})

		if temp and result:
			for row in self.aspecto_microscopico:
				for tmp in temp:
					if row.indice_urinario == tmp.indice_urinario:
						row.examen_fisicoquimico = tmp.examen_fisicoquimico
		
		return True
	
	def get_depuracion_creatinina(self):
		temp = self.indices_pruebas if hasattr(self,'depuracion_creatinina_table') else 0.00 

		result = frappe.db.sql("""SELECT C.prueba AS name, I.prueba_nombre AS prueba, I.uds, I.metodo,I.name as indice,I.rango_por_edad, I.rango_referencia AS rango_ref
			FROM 
				`tabIndice Prueba` I JOIN `{0}` C 
			ON 
				I.prueba = C.prueba 
			WHERE 
				C.parent = '{1}' AND I.grupo = 'QUIMICA'  AND C.prueba = 'PRB-000000149'
			ORDER BY C.idx"""
			.format(self.get_consult_table(), self.consulta),
		as_dict=True)
		frappe.errprint(result)
		self.depuracion_creatinina_table = []
		self.test_prb_000000149 = 1 if result else 0
		for prueba in result:
			if (prueba.rango_por_edad):
				prueba.rango_ref = get_rango_por_edad(prueba.indice, self.edad)

			self.append("depuracion_creatinina_table",{"prueba":"DIURESIS","metodo":"-","rango_ref":" ","uds":"ML/24 Horas"})
			self.append("depuracion_creatinina_table",{"prueba":"SUPERFICIE CORPOREA","metodo":"-","rango_ref":" ","uds":" "})
			self.append("depuracion_creatinina_table",{"prueba":"CREATININA EN SUERO","metodo":"-","rango_ref":"0.6 - 1.2","uds":"MG/DL"})
			self.append("depuracion_creatinina_table",{"prueba":"CREATININA ORINA","metodo":"-","rango_ref":" ","uds":"MG/DL"})
			self.append("depuracion_creatinina_table",{"prueba":"CREATININA ORINA 24 HRS","metodo":"-","rango_ref":"1.0 - 1.5","uds":"ML/MIN"})
			self.append("depuracion_creatinina_table",{"prueba":"DCE","metodo":"-","rango_ref":" ","uds":"ML/MIN"})
			self.append("depuracion_creatinina_table",{"prueba":"DCE CORREGIDA","metodo":"-","rango_ref":"98 - 156","uds":"ML/MIN"})
		
		if temp and result:
			for row in self.depuracion_creatinina_table:
				for tmp in temp:
					if row.prueba == tmp.prueba:
						row.resultado = tmp.resultado
		return True
	
	def get_digestion_heces(self):
		temp = self.aspecto_fisico_heces if hasattr(self,'aspecto_fisico_heces') else 0.00 
		self.aspecto_fisico_heces = []
		filters = {"disponible": 1, "digestion_heces":1, "tipo_indice":"Aspecto Fisico"}
		result = frappe.get_list("Indice Urinario", filters,["nombre"],order_by="creation ASC",limit_page_length=0)
		tiene_digestion_heces = frappe.db.sql("""SELECT prueba from `{0}` WHERE parent='{1}' AND prueba = 'PRB-000000210' """  
			.format(self.get_consult_table(), self.consulta), as_dict=True)
		 
		self.test_digestion_heces = 1 if result and tiene_digestion_heces else 0	
		for indice in result:
		
			self.append("aspecto_fisico_heces",{
				"indice_urinario": indice.nombre, 
			})

		if temp and result:
			for row in self.aspecto_fisico_heces:
				for tmp in temp:
					if row.indice_urinario == tmp.indice_urinario:
						row.examen_fisicoquimico = tmp.examen_fisicoquimico

		temp = self.aspecto_microscopico_heces  if hasattr(self,'aspecto_microscopico_heces') else 0.00 
		self.aspecto_microscopico_heces = []	
		filters = {"disponible": 1, "digestion_heces":1, "tipo_indice":"Aspecto Microscopico"}
		result = frappe.get_list("Indice Urinario", filters, ["nombre"], order_by="nombre ASC")
		for indice in result:
			frappe.errprint(indice.nombre)
			self.append("aspecto_microscopico_heces",{
				"indice_urinario": indice.nombre, 
				#"examen_fisicoquimico":""
				
			})

		if temp and result:
			for row in self.aspecto_microscopico_heces:
				for tmp in temp:
					if row.indice_urinario == tmp.indice_urinario:
						row.examen_fisicoquimico = tmp.examen_fisicoquimico
		
		return True
	
	def get_anexos(self):
		self_dict = self.as_dict()
		consulta = frappe.get_doc(self.consulta_tipo, self.consulta)
		# centinela para mostrar o no el section break de anexos
		show_anexos = 0 
		for prueba in consulta.pruebas:
			anexos = frappe.get_list(
				"Anexo", 
				{"prueba":prueba.prueba}, 
				[
					"descripcion",
					"metodo",
					"rango_referencia",
					"uds",
					"es_una_tabla",
					"interpretacion"
				], order_by = "indice")
			# No se le reporta Anexos a la TSH si el paciente es hombre
			# if prueba.prueba == "PRB-000000065" and self.sexo == "MASCULINO":
				# continue
			
			self.quimica_observaciones =  ''
			
			if prueba.prueba == "PRB-000000287":
				show_anexos = 1
			
			if anexos and anexos[0].es_una_tabla:
				# frappe.errprint(anexos)
				show_anexos = 1
				tbl_anexo = (prueba.prueba).replace("-","_").lower()
				self.set(tbl_anexo,[]) # limpia el child table correspondiente
				self.set("test_" + tbl_anexo, 1) # set visible the table and the heading

				if prueba.prueba == "PRB-000000285":
					self.append(tbl_anexo, {"fraction": "ALBUMINA", "percent1": 57.6, "percent2": 47.6, "range_1": 61.9})
					self.append(tbl_anexo, {"fraction": "ALFA 1", "percent1": 3.0, "percent2": 1.4, "range_1": 4.6})
					self.append(tbl_anexo, {"fraction": "ALFA 2", "percent1": 7.8, "percent2": 7.3, "range_1": 13.9})
					self.append(tbl_anexo, {"fraction": "BETA", "percent1": 11.4, "percent2": 10.9, "range_1": 19.1})
					self.append(tbl_anexo, {"fraction": "GAMMA", "percent1": 20.1, "percent2": 9.5, "range_1": 24.8})

				for anexo in anexos:
					if self_dict.has_key(tbl_anexo):
						self.append(tbl_anexo, anexo)
				# 	if prueba.prueba == "PRB-000000285":
				# 		self.append(tbl_anexo, {"fraction": "TOTAL", "percent1": " ", "percent2": " ", "range1": " ", "range2": " "})

			elif anexos:
				# Prueba del COVID-19 para que salga en una pagina
				if prueba.prueba == "PRB-000000317":
					self.quimica_observaciones = anexos[0].interpretacion if not self.quimica_observaciones else \
						"<br>{}".format(anexos[0].interpretacion)
				# Prueba del COVID-19 para que salga en una pagina
				elif prueba.prueba == "PRB-000000326":
					self.quimica_observaciones = anexos[0].interpretacion if not self.quimica_observaciones else \
						"<br>{}".format(anexos[0].interpretacion)
				elif prueba.prueba == "PRB-000000339":
					self.quimica_observaciones = anexos[0].interpretacion if not self.quimica_observaciones else \
						"<br>{}".format(anexos[0].interpretacion)

				else:
					self.otros_anexos = 1
					self.otros_title = anexos[0].descripcion
					self.otros_descripcion = anexos[0].interpretacion
			self.test_anexos = show_anexos 
		# frappe.errprint("{} {}".format(self.test_anexos, self.test_prb_000000065))
		return True
	
	def get_others(self):
		self.get_digestion_heces()
		self.get_depuracion_creatinina()

	def has_urianalisis(self):

		tipo_cons = "Consulta Prueba Privada" if self.consulta_tipo == "Consulta Privada" else "Consulta Prueba"
		return not not frappe.get_value(tipo_cons, {'parent':self.consulta, 'prueba':'PRB-000000229'})

	def get_especiales(self):
		result = frappe.db.sql("""SELECT I.prueba_nombre AS prueba, I.uds, I.metodo, I.rango_referencia AS rango_ref
			FROM 
				`tabIndice Prueba` I JOIN `{0}` C 
			ON 
				I.prueba = C.prueba 
			WHERE 
				C.parent = '{1}' AND I.grupo  = 'ESPECIALES'
			ORDER BY C.idx"""
			.format(self.get_consult_table(), self.consulta),
		as_dict=True)

		self.test_especiales = 1 if result else 0

		for prueba in result:
			self.resultados_especiales = """
				<div><br></div><div><b>Biología Molecular</b></div><div><br></div><div><b>Factor V Leiden</b>. .c. 1601G&gt;A. .mutación. ...<b>[Colocar Resultado]</b></div><div>Muestra: Sangre completa colectada con EDIA</div><div>Metodología: PCR IR</div><div><b><br></b></div><div><b>Nota:</b></div><div>La variante del factor V Leiden (p.Arg534GIn) es un factor de riesgo leve de tromboembolismo venoso. Aunque la variante del factor V de Leiden está ausente, el individuo puede tener otros factores de riesgo genéticos y ambientales de tromboembolismo venoso.</div><div>Discrepancias entre el ensayo de resistencia a la proteína C activada y la mutación del Factor V Leiden c.1601 G&gt;A, puede observarse en pacientes que han recibido trasplantes alogénicos de células madre o trasplantes de hígado.</div>
			"""
		return True

	def get_table_items(self):
		self.refresh_personal_info()
		self.get_quimica()
		self.get_serologia()
		self.get_inmunodiagnostico()
		self.get_hormonas()
		self.get_tipificacion()
		self.get_hematologia()
		self.get_urianalisis()
		self.get_otros_uroanalisis()
		self.get_coprologia()
		self.get_anexos()
		self.get_microbiologia()
		self.get_espermatograma()
		self.get_others()
		self.get_especiales()
