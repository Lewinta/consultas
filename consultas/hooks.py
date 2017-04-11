# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "consultas"
app_title = "Consultas"
app_publisher = "Lewin Villar"
app_description = "Consultas de Pacientes Laboratorio Clinico"
app_icon = "octicon octicon-beaker"
app_color = "grey"
app_email = "lewin.villar@gmail.com"
app_license = "MIT"

#website
app_include_js = [
"assets/js/user_functions.js"
#        "assets/js/libs.min.js",
#        "assets/js/desk.min.js",
#        "assets/js/editor.min.js",
#        "assets/js/list.min.js",
#        "assets/js/form.min.js",
#        "assets/js/report.min.js",
#        "assets/js/d3.min.js",
#        #"assets/js/user_functions.js",
#        "assets/frappe/js/frappe/toolbar.js"
]
#app_include_css = [
#        "assets/css/desk.min.css",
#        "assets/css/list.min.css",
#        "assets/css/form.min.css",
#        "assets/css/report.min.css",
#        "assets/css/module.min.css"
#]




# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/consultas/css/consultas.css"
# app_include_js = "/assets/consultas/js/consultas.js"

# include js, css files in header of web template
# web_include_css = "/assets/consultas/css/consultas.css"
# web_include_js = "/assets/consultas/js/consultas.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "consultas.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "consultas.install.before_install"
# after_install = "consultas.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "consultas.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"consultas.tasks.all"
# 	],
# 	"daily": [
# 		"consultas.tasks.daily"
# 	],
# 	"hourly": [
# 		"consultas.tasks.hourly"
# 	],
# 	"weekly": [
# 		"consultas.tasks.weekly"
# 	]
# 	"monthly": [
# 		"consultas.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "consultas.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "consultas.event.get_events"
# }

