app_name = "vin_isipl"
app_title = "Vin Isipl"
app_publisher = "Vintrosys"
app_description = "Vin Isipl"
app_email = "admin@vintrosys.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "vin_isipl",
# 		"logo": "/assets/vin_isipl/logo.png",
# 		"title": "Vin Isipl",
# 		"route": "/vin_isipl",
# 		"has_permission": "vin_isipl.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/vin_isipl/css/vin_isipl.css"
# app_include_js = "/assets/vin_isipl/js/vin_isipl.js"

# include js, css files in header of web template
# web_include_css = "/assets/vin_isipl/css/vin_isipl.css"
# web_include_js = "/assets/vin_isipl/js/vin_isipl.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "vin_isipl/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "vin_isipl/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
jinja = {"methods": "vin_isipl.utils.jinja"}

# Print Format - PDF
pdf_footer_html = "vin_isipl.utils.pdf.pdf_footer_html"

# Installation
# ------------

# before_install = "vin_isipl.install.before_install"
after_install = "vin_isipl.install.after_install"

# Uninstallation
# ------------

before_uninstall = "vin_isipl.uninstall.before_uninstall"
# after_uninstall = "vin_isipl.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "vin_isipl.utils.before_app_install"
# after_app_install = "vin_isipl.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "vin_isipl.utils.before_app_uninstall"
# after_app_uninstall = "vin_isipl.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "vin_isipl.notifications.get_notification_config"

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

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"vin_isipl.tasks.all"
# 	],
# 	"daily": [
# 		"vin_isipl.tasks.daily"
# 	],
# 	"hourly": [
# 		"vin_isipl.tasks.hourly"
# 	],
# 	"weekly": [
# 		"vin_isipl.tasks.weekly"
# 	],
# 	"monthly": [
# 		"vin_isipl.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "vin_isipl.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "vin_isipl.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "vin_isipl.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["vin_isipl.utils.before_request"]
# after_request = ["vin_isipl.utils.after_request"]

# Job Events
# ----------
# before_job = ["vin_isipl.utils.before_job"]
# after_job = ["vin_isipl.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"vin_isipl.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

