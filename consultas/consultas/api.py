import frappe, json

from frappe.utils import get_url

@frappe.whitelist(allow_guest=True)
def get_results(filters):
	filters = frappe._dict(json.loads(filters))

	return frappe.db.sql("""SELECT name, docstatus, fecha, paciente, print_url
		FROM `tabResultado`
		WHERE 1 = 1
		%(conditions)s
		ORDER BY fecha, paciente, docstatus""" % {
			"conditions": get_conditions(filters)
		}, as_dict=True, debug=True)

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
