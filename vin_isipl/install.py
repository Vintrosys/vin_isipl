from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def after_install():
	create_custom_fields(get_custom_fields())
	
def get_custom_fields():
	return {
		"Company": [
			{
				"fieldname": "quotation_left_logo",
				"fieldtype": "Attach Image",
				"label": "Quotation Left Logo",
				"insert_after": "parent_company",
			},
		],
		"Quotation Item": [
			{
				"fieldname": "stock_status",
				"fieldtype": "Select",
				"label": "Stock Status",
				"options": "\nAvailable\nPartially Available\nNot Available",
				"insert_after": "prevdoc_docname",
			}
		]
	}