from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def after_install():
	create_custom_fields(get_custom_fields())
	
def get_custom_fields():
	return {
		"Company": [
			{
				"fieldname": "machine_brand_logo",
				"fieldtype": "Attach Image",
				"label": "Machine Brand Logo",
				"insert_after": "parent_company",
			},
			{
				"fieldname": "company_seal_image",
				"fieldtype": "Attach Image",
				"label": "Company Seal Image",
				"insert_after": "machine_brand_logo",
			}
		],
		"Quotation": [
			{
				"fieldname": "sales_person",
				"fieldtype": "Link",
				"label": "Sales Person",
				"options": "Sales Person",
				"insert_after": "valid_till",
			}
		],
		"Quotation Item": [
			{
				"fieldname": "stock_status",
				"fieldtype": "Select",
				"label": "Stock Status",
				"options": "\nAvailable\nPartially Available\nNot Available",
				"insert_after": "prevdoc_docname",
			},
			{
				"fieldname": "machine_code",
				"fieldtype": "Data",
				"label": "Machine Code",
				"insert_after": "item_code",
			}
		],
		"Shipping Rule": [
			{
				"fieldname": "section_break_dis_des",
				"fieldtype": "Section Break",
				"insert_after": "shipping_rule_type",
			},
			{
				"fieldname": "port_of_discharge",
				"fieldtype": "Data",
				"label": "Port of Discharge",
				"insert_after": "section_break_dis_des",
			},
			{
				"fieldname": "column_break_dis_des",
				"fieldtype": "Column Break",
				"insert_after": "port_of_discharge",
			},
			{
				"fieldname": "final_destination",
				"fieldtype": "Data",
				"label": "Final Destination",
				"insert_after": "column_break_dis_des",
			}
		],
		"Sales Person": [
			{
				"fieldname": "signature_image",
				"fieldtype": "Attach Image",
				"label": "Signature Image",
				"insert_after": "department",
			}
		]
	}