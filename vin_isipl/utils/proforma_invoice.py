import frappe
from vin_isipl.utils.pdf import attach_pdf

def on_update(doc, method=None):
    
    print_format_map = {
        "Stock PI": "Machine PI",
        "Import PI": "Import PI",
        "Spares PI": "Spares PI",
        "Service PI": "Service PI"
    }
       
    frappe.enqueue(
        method="vin_isipl.utils.pdf.attach_pdf",
        queue='long',
        timeout=300,
        job_name=f"Attach PDF for {doc.doctype} {doc.name}",
        doc=doc,
        print_format_map=print_format_map
    )
