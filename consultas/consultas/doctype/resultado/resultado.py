	# -*- coding: utf-8 -*-
# Copyright (c) 2017, Lewin Villar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Resultado(Document):
		
	# def refresh_coprologico(self):
	# 	self.aspecto_fisico = []
	# 	filters = {"disponible": 1, "coprologico":1, "tipo_indice":"Aspecto Fisico"}
	# 	for indice in frappe.get_list("Indice Urinario", filters,["nombre"],order_by="creation ASC",limit_page_length=0):
		
	# 		self.append("aspecto_fisico",{
	# 			"indice_urinario": indice.nombre, 
	# 			#"examen_fisicoquimico":""
				
	# 		})
	# 	self.aspecto_microscopico = []	
	# 	filters = {"disponible": 1, "coprologico":1, "tipo_indice":"Aspecto Microscopico"}
	# 	for indice in frappe.get_list("Indice Urinario", filters, ["nombre"], order_by="creation ASC", limit_page_length=0):
		
	# 		self.append("aspecto_microscopico",{
	# 			"indice_urinario": indice.nombre, 
	# 			#"examen_fisicoquimico":""
				
	# 		})
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
	def assign_result_to_consult(self):	
		# Remove Resultado to Consulta Privada
		cp = frappe.get_doc(self.consulta_tipo, self.consulta)
		cp.resultado = ""
		cp.db_update()

	def on_cancel(self):
		self.assign_result_to_consult()

	def on_trash(self):
		self.assign_result_to_consult()

	def after_insert(self):
		# Assign Resultado to Consulta Privada
		cp = frappe.get_doc(self.consulta_tipo, self.consulta)
		cp.resultado = self.name
		cp.db_update()

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

		result = frappe.db.sql("""SELECT C.prueba AS name, I.prueba_nombre AS prueba, I.uds, I.metodo, I.rango_referencia AS rango_ref
			FROM 
				`tabIndice Prueba` I JOIN `{0}` C 
			ON 
				I.prueba = C.prueba 
			WHERE 
				C.parent = '{1}' AND I.grupo = 'QUIMICA'"""
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
				self.append("indices_pruebas",{"prueba":"HIERRO TOTAL","metodo":"  ","rango_ref":"50 - 212","uds":"ug/DL"})
				self.append("indices_pruebas",{"prueba":"T I B C","metodo":"  ","rango_ref":"205 - 567","uds":"ug/DL"})
				self.append("indices_pruebas",{"prueba":"% de Saturation","metodo":"  ","rango_ref":"24.3 - 37.4","uds":"%"})
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
		result = frappe.db.sql("""SELECT C.prueba AS name, I.prueba_nombre AS prueba, I.uds, I.metodo, I.rango_referencia AS rango_ref
			FROM 
				`tabIndice Prueba` I JOIN `{0}` C 
			ON 
				I.prueba = C.prueba 
			WHERE 
				C.parent = '{1}' AND I.grupo = 'SEROLOGIA'"""
			.format(self.get_consult_table(), self.consulta),
		as_dict=True)
		
		self.serologia = []
		self.test_serologia = 1 if result else 0
		for prueba in result:
			self.append("serologia",prueba)

		if temp and result:
			for row in self.serologia:
				for tmp in temp:
					if row.prueba == tmp.prueba:
						row.resultado = tmp.resultado
		return True

	def get_inmunodiagnostico(self):
		temp = self.inmunodiagnosticos if hasattr(self,'inmunodiagnosticos') else 0.00 
		result = frappe.db.sql("""SELECT C.prueba AS name, I.prueba_nombre AS prueba, I.uds, I.metodo, I.rango_referencia AS rango_ref
			FROM 
				`tabIndice Prueba` I JOIN `{0}` C 
			ON 
				I.prueba = C.prueba 
			WHERE 
				C.parent = '{1}' AND I.grupo = 'INMUNODIAGNOSTICOS'
			AND C.prueba <>'PRB-000000224'"""
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
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba": " ", "metodo": "CONTROL", "rango_ref": "          ", "uds": "SEGUNDOS"})	
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba": " ", "metodo": "INR"    , "rango_ref": "0.9 - 1.2" , "uds": "SEGUNDOS"})	
				self.append("inmunodiagnosticos",{"prueba_name": prueba.prueba_name, "prueba": " ", "metodo": "%"      , "rango_ref": "70 - 120"," uds":"%"})	
				continue 

			if prueba.name == "PRB-000000060":
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
			
			self.append("inmunodiagnosticos",prueba)

	def get_espermatograma(self):
		temp_examen_macroscopico = self.examen_macroscopico if hasattr(self,'examen_macroscopico') else 0.00 
		temp_examen_microscopico = self.examen_microscopico if hasattr(self,'examen_microscopico') else 0.00 
		temp_evaluacion_mortalidad = self.evaluacion_mortalidad if hasattr(self,'evaluacion_mortalidad') else 0.00 
		temp_concentracion = self.concentracion if hasattr(self,'concentracion') else 0.00 
		temp_morfologia_espermatica = self.morfologia_espermatica if hasattr(self,'morfologia_espermatica') else 0.00 
		result = frappe.db.sql("""SELECT prueba  from `{0}` WHERE parent='{0}' AND prueba  = 'PRB-000000268'"""
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
				C.parent = '{1}' AND I.grupo  = 'MICROBIOLOGIA'"""
			.format(self.get_consult_table(), self.consulta), as_dict=True)

		self.antibiogramas = []
		self.test_microbiologia = 1 if result else 0 
		for prueba in result:
			if prueba.prueba_name == "PRB-000000188":
				self.tipo_cultivo = "SECRECION DE OIDO IZQUIERDO"

			if prueba.prueba_name == "PRB-000000260":
				self.tipo_cultivo = "SECRECION DE OIDO DERECHO"

			if prueba.prueba_name == "PRB-000000191":
				self.tipo_cultivo = "SECRECION URETRAL"

			if prueba.prueba_name == "PRB-000000187":
				self.tipo_cultivo = "SECRECION FORUNCULOS"

			if prueba.prueba_name == "PRB-000000261":
				self.tipo_cultivo = "ESPUTO"
				self.tipo_microbiologia = "BACILOSCOPIA"

			if prueba.prueba_name == "PRB-000000192":
				self.tipo_cultivo = "MATERIA FECAL"

			if prueba.prueba_name == "PRB-000000267":
				self.tipo_cultivo = "SEMEN"
				return 0

			if prueba.prueba_name == "PRB-000000194":
				self.tipo_cultivo = "SECRECION DE OIDO"
				
			if prueba.prueba_name == "PRB-000000189":
				self.append("bacteriologia_vaginal", {"valor": "BACTERIAS", "resultado": "", "interpretacion": "-"})	
				self.append("bacteriologia_vaginal", {"valor": "CELULAS EPITELIALES", "resultado": "", "interpretacion": "-" })	
				self.append("bacteriologia_vaginal", {"valor": "LEUCOCITOS", "resultado": "", "interpretacion": "-" })	
				self.append("bacteriologia_vaginal", {"valor": "LEVADURAS", "resultado": "", "interpretacion": "-" })	
				self.append("bacteriologia_vaginal", {"valor": "TRICHOMONAS", "resultado": "", "interpretacion": "-" })
				self.tipo_cultivo = "SECRECION VAGINAL"

			self.append("antibiogramas", {"valor": "CIPROFLOXACIN", "resultado": "", "interpretacion": "-"})	
			self.append("antibiogramas", {"valor": "BENZILPENCILLINS", "resultado": "", "interpretacion": "-" })	
			self.append("antibiogramas", {"valor": "CLINDAMYCIN", "resultado": "", "interpretacion": "-" })	
			self.append("antibiogramas", {"valor": "ERITROMICIN", "resultado": "", "interpretacion": "-" })	
			self.append("antibiogramas", {"valor": "GENTAMICIN", "resultado": "", "interpretacion": "-" })
			self.append("antibiogramas", {"valor": "LEVOFLOXACIN", "resultado": "", "interpretacion": "-" })
			self.append("antibiogramas", {"valor": "LINEZOLID", "resultado": "", "interpretacion": "-" })
			self.append("antibiogramas", {"valor": "MOXIFLOXACIN", "resultado": "", "interpretacion": "-" })
			self.append("antibiogramas", {"valor": "NITROFURANTOIN", "resultado": "", "interpretacion": "-" })
			self.append("antibiogramas", {"valor": "QUINUPRI/DALFOPRI", "resultado": "", "interpretacion": "-" })
			self.append("antibiogramas", {"valor": "RIFAMPICIN", "resultado": "", "interpretacion": "-" })
			self.append("antibiogramas", {"valor": "T. SULFA", "resultado": "", "interpretacion": "-" })
			self.append("antibiogramas", {"valor": "TETRACYCLINE", "resultado": "", "interpretacion": "-" })
			self.append("antibiogramas", {"valor": "TIGECICLINAS", "resultado": "", "interpretacion": "-" })
			self.append("antibiogramas", {"valor": "VACOMYCIN", "resultado": "", "interpretacion": "-" })
			self.append("antibiogramas", {"valor": "CEFOXITIN", "resultado": "", "interpretacion": "-" })


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
		result = frappe.db.sql("""SELECT C.prueba AS name, I.prueba_nombre AS prueba, I.uds, I.metodo, I.rango_referencia AS rango_ref
			FROM 
				`tabIndice Prueba` I JOIN `{0}` C 
			ON 
				I.prueba = C.prueba 
			WHERE 
				C.parent = '{1}' AND I.grupo  = 'HORMONAS'"""
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
		temp = self.indices_hematologicos if hasattr(self,'indices_hematologicos') else 0.00 
		result = frappe.db.sql("""SELECT prueba from `{0}` WHERE parent='{1}' AND prueba in ('PRB-000000195') """  
			.format(self.get_consult_table(), self.consulta),
		as_dict=True)

		self.indices_hematologicos = []
		self.test_hematologico = 1 if result else 0	
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
		result = frappe.get_list("Indice Urinario", {"disponible": 1,"sedimento_urinario":1},["nombre"],order_by="creation ASC",limit_page_length=0)
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
		result = frappe.get_list("Indice Urinario", filters, ["nombre"], order_by="creation ASC", limit_page_length=0)
		for indice in result:
		
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
	def get_anexos(self):

		consulta = frappe.get_doc(self.consulta_tipo, self.consulta)
		# centinela para mostrar o no el section break de anexos
		show_anexos = 0 
		for prueba in consulta.pruebas:
			anexos = frappe.get_list("Anexo", {"prueba":prueba.prueba}, ["descripcion", "metodo", "rango_referencia", "uds", "es_una_tabla", "interpretacion"], order_by = "indice")
			if anexos and anexos[0].es_una_tabla:
				show_anexos = 1
				tbl_anexo = (prueba.prueba).replace("-","_").lower()
				self.set(tbl_anexo,[]) # limpia el child table correspondiente
				self.set("test_"+tbl_anexo,1) # set visible the table and the heading
				
				for anexo in anexos:
					self.append(tbl_anexo, anexo)
			elif anexos:
				self.otros_anexos = 1
				self.otros_title = anexos[0].descripcion
				self.otros_descripcion = anexos[0].interpretacion
			self.test_anexos = show_anexos 

		return True
	def has_urianalisis(self):

		tipo_cons = "Consulta Prueba Privada" if self.consulta_tipo == "Consulta Privada" else "Consulta Prueba"
		return not not frappe.get_value(tipo_cons, {'parent':self.consulta, 'prueba':'PRB-000000229'})

	def get_table_items(self):
		self.refresh_personal_info()
		self.get_quimica()
		self.get_serologia()
		self.get_inmunodiagnostico()
		self.get_hormonas()
		self.get_tipificacion()
		self.get_hematologia()
		self.get_urianalisis()
		self.get_coprologia()
		self.get_anexos()
		self.get_microbiologia()
		self.get_espermatograma()
