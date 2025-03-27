import frappe
from frappe.utils.pdf import get_pdf
from frappe.utils import now

@frappe.whitelist()
def save_to_table(quotation_name):
    quotation = frappe.get_doc('Quotation', quotation_name)
    
    print_format = ""
    if quotation.order_type == "STKPI":
        print_format = "Machine PI"
    elif quotation.order_type == "IMPPI":
        print_format = "Import PI"
    elif quotation.order_type == "SPPI":
        print_format = "Spares PI"
    elif quotation.order_type == "SRPI":
        print_format = "Service PI"
    pdf_data = get_pdf(frappe.get_print('Quotation', quotation_name, print_format))

    file_doc = frappe.get_doc({
        'doctype': 'File',
        'file_name': f"{quotation_name}.pdf",
        'content': pdf_data,
        'is_private': 1
    }).insert(ignore_permissions=True)

    quotation.append('custom_pi_version_tracker', {
        'created_by': frappe.session.user,
        'created_on': now(),
        'pdf_attachment': file_doc.file_url
    })

    quotation.save(ignore_permissions=True)
