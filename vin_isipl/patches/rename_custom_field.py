import frappe

def execute():
	frappe.db.rename_column("Company", "quotation_left_logo", "machine_brand_logo")
	frappe.db.delete(
		"Custom Field",
		{
			"fieldname": ("in", ["quotation_left_logo"]),
			"dt": "Company",
		},
	)