import frappe
from frappe.utils.jinja_globals import is_rtl


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
