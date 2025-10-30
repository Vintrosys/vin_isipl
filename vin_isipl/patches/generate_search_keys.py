import re
import frappe

def sanitize(s):
    return re.sub(r'[^a-zA-Z0-9]', '', (s or '')).lower()

# Currently search optimization done only for Item, Customer, Supplier
def execute():
    
    items = frappe.get_all("Item", fields=["name", "item_code"])
    for item in items:
        clean = sanitize(item.item_code)
        frappe.db.set_value("Item", item.name, "custom_search_key", clean)

    customers = frappe.get_all("Customer", fields=["name", "customer_name"])
    for customer in customers:
        clean = sanitize(customer.customer_name)
        frappe.db.set_value("Customer", customer.name, "custom_search_key", clean)

    suppliers = frappe.get_all("Supplier", fields=["name", "supplier_name"])
    for supplier in suppliers:
        clean = sanitize(supplier.supplier_name)
        frappe.db.set_value("Supplier", supplier.name, "custom_search_key", clean)

    hd_customers = frappe.get_all("HD Customer", fields=["name", "customer_name"])
    for hd_customer in hd_customers:
        clean = sanitize(hd_customer.customer_name)
        frappe.db.set_value("HD Customer", hd_customer.name, "custom_search_key", clean)
    frappe.db.commit()