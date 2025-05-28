import frappe
from frappe.utils.jinja_globals import is_rtl
from frappe.utils.pdf import get_pdf


def pdf_footer_html(soup, head, content, styles, html_id, css):
	return frappe.render_template(
		"templates/print_formats/vin_pdf_header_footer.html",
		{
			"head": head,
			"content": content,
			"styles": styles,
			"html_id": html_id,
			"css": css,
			"lang": frappe.local.lang,
			"layout_direction": "rtl" if is_rtl() else "ltr",
		},
	)



def attach_pdf(doc, print_format_map):
    doctype = doc.doctype
    name = doc.name

    key = doc.get("order_type") or doc.get("company")

    print_format = print_format_map.get(key) or print_format_map.get("*")

    pdf_data = get_pdf(frappe.get_print(doctype, name, print_format))

    file_doc = frappe.get_doc({
        'doctype': 'File',
        'file_name': f"{name}.pdf",
        'content': pdf_data,
        'is_private': 1,
        'attached_to_doctype': doctype,
        'attached_to_name': name
    }).insert(ignore_permissions=True)

    frappe.db.set_value(doctype, name, "custom_print_pdf", file_doc.file_url, update_modified=False )

