import frappe

def before_insert(doc, method=None):
    dt = frappe.utils.now_datetime()
    doc.created_on_date = dt.date()
    doc.created_on_time = dt.time().replace(microsecond=0)

def before_save(doc, method=None):
    dt = frappe.utils.now_datetime()
    doc.custom_last_modified_date = dt.date()
    doc.custom_last_modified_time = dt.time().replace(microsecond=0)
