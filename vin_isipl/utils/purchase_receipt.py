import frappe
from frappe.core.doctype.user.user import flt
from vin_isipl.utils.pdf import attach_pdf


def on_update(doc, method=None):
    
    print_format_map = {
        "*": "ISIPL GRN"
    }
    
    frappe.enqueue(
        method="vin_isipl.utils.pdf.attach_pdf",
        queue='long',
        timeout=300,
        job_name=f"Attach PDF for {doc.doctype} {doc.name}",
        doc=doc,
        print_format_map=print_format_map
    )

def validate(doc, method=None):
    for item in doc.items:
        item.custom_balance_quantity = flt(item.custom_total_qty) - flt(item.qty)

