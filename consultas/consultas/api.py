import frappe, json

from frappe.utils import get_url
from frappe.utils.pdf import get_pdf
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_results(filters):
	filters = frappe._dict(json.loads(filters))

	return frappe.db.sql("""SELECT name, docstatus, fecha, paciente, institucion, print_url
		FROM `tabResultado`
		WHERE docstatus != 2
 		%(conditions)s
		ORDER BY fecha, paciente, docstatus""" % {
			"conditions": get_conditions(filters)
		}, as_dict=True, debug=True)

@frappe.whitelist(allow_guest=True)
def get_institutions(medico):
	if not medico:
		return frappe.db.sql("""SELECT name
			FROM `tabInstitucion`
			WHERE pertenece_a_la_pagina = 1
			ORDER BY name""", debug=False
		)
	else:
		return frappe.db.sql("""
			SELECT
				distinct(`tabResultado`.institucion) as name
			FROM
				`tabResultado`
			JOIN
				`tabInstitucion`
			ON
				`tabResultado`.institucion = `tabInstitucion`.name
			WHERE
				`tabInstitucion`.pertenece_a_la_pagina = 1
			AND
				`tabResultado`.medico = %s
			ORDER BY name""", medico, debug=False
		)


@frappe.whitelist(allow_guest=True)
def get_print_url(name, print_format="Resultados Timbrados"):
	doc = frappe.get_doc("Resultado", name)
	return "{url}/{doctype}/{name}?format={print_format}&key={key}".format(**{
		"url": get_url(),
		"doctype": "Resultado",
		"name": name,
		"print_format": print_format,
		"key": doc.get_signature()
	})

@frappe.whitelist(allow_guest=True)
def get_team(email):
	return frappe.db.get_value("Institucion", {
		"correo_electronico": email
	})
	

@frappe.whitelist(allow_guest=True)
def get_single_result(key):
	name = frappe.db.exists("Resultado", {"key":key, "docstatus": 1})
	if not name:
		return False
	url = "https://app.laboratoriobetalab.com/api/method/consultas.consultas.api.download_result_pdf?key_code={}".format(key)
	return url

@frappe.whitelist(allow_guest=True)
def download_result_pdf(key_code, format="Resultados Timbrados", no_letterhead=0):
	doctype = "Resultado"
	
	name = frappe.db.exists(doctype, {"key": key_code})
	if not name:
		frappe.local.response["type"] = "redirect"
		frappe.local.response["location"] = "/custom_404.html?key_code={}".format(key_code[0:-6])
	else:	
		html = frappe.get_print(doctype, name, format, no_letterhead=no_letterhead)
		frappe.local.response.filename = "{name}.pdf".format(name=name.replace(" ", "-").replace("/", "-"))
		frappe.local.response.filecontent = get_pdf(html)
		frappe.local.response.type = "download"
	
def get_conditions(filters):
	query = []

	filters.get("start_date") and query.append("AND fecha >= '{start_date}'")
	filters.get("end_date") and query.append("AND fecha <= '{end_date}'")
	filters.get("paciente") and query.append("AND paciente LIKE '%{paciente}%'")
	filters.get("medico") and query.append("AND medico = '{medico}'")
	filters.get("sucursal") and query.append("AND sucursal = '{sucursal}'")
	filters.get("institucion") and query.append("AND institucion = '{institucion}'")
	filters.get("docstatus") and query.append("AND docstatus = '{docstatus}'")

	return " ".join(query).format(**filters)

def borrador(doctype, docname):
	doc = frappe.get_doc(doctype,docname)
	doc.docstatus = 0
	doc.db_update()
	frappe.db.commit()

def quitar_coprologico(docname):
	doc = frappe.get_doc("Resultado",docname)
	if doc:
		doc.test_coprologico = 0
		print("removed coprologico")
	doc.db_update()
	frappe.db.commit()

def get_rango_por_edad(indice_prueba, edad):
	if not frappe.db.exists("Indice Prueba", indice_prueba):
		return "not found"
	# ip = frappe.get_value("Indice Prueba", {"prueba": prueba}, "name")

	conditions = frappe.db.sql("""
		SELECT
			condicion,
			edad_anos,
			rango_de_referencia
		FROM 
			`tabRango por Edad`
		WHERE
			parent = %s
		""", indice_prueba, as_dict=True)

	for cond in conditions:
		# print(cond.condicion)
		if cond.condicion == "Menor":
			frappe.errprint("{} {} < {}".format(cond.condicion, cond.edad_anos, edad))
			if edad < cond.edad_anos :
				return cond.rango_de_referencia

		if cond.condicion == "Igual":
			frappe.errprint("{} {} == {}".format(cond.condicion, cond.edad_anos, edad))
			if edad == cond.edad_anos:
				return cond.rango_de_referencia

		if cond.condicion == "Mayor":
			frappe.errprint("{} {} > {}".format(cond.condicion, cond.edad_anos, edad))
			if edad > cond.edad_anos:
				return cond.rango_de_referencia
	
	return " - "
