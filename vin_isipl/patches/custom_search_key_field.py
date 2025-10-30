import frappe

def execute():
    fields_to_create = [
        {
            "dt": "Item",
            "fieldname": "custom_search_key",
            "label": "Search Key",
            "insert_after": "item_code"
        },
        {
            "dt": "Customer",
            "fieldname": "custom_search_key",
            "label": "Search Key",
            "insert_after": "customer_name"
        },
        {
            "dt": "Supplier",
            "fieldname": "custom_search_key",
            "label": "Search Key",
            "insert_after": "supplier_name"
        },
        {
            "dt": "HD Customer",
            "fieldname": "custom_search_key",
            "label": "Search Key",
            "insert_after": "customer_name"
        }
    ]

    for field in fields_to_create:
        if not frappe.db.exists("Custom Field", {"dt": field["dt"], "fieldname": field["fieldname"]}):
            custom_field = frappe.get_doc({
                "doctype": "Custom Field",
                "dt": field["dt"],
                "fieldname": field["fieldname"],
                "label": field["label"],
                "fieldtype": "Data",
                "insert_after": field["insert_after"],
                "hidden": 1,
                "read_only": 1,
                "no_copy": 1
            })
            custom_field.insert()
            print(f"Created custom field: {field['fieldname']} in {field['dt']}")

    frappe.db.commit()