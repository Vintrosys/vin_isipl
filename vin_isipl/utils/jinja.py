from phonenumbers import PhoneNumberFormat, format_number, is_valid_number, parse
from frappe.utils.formatters import format_value as _format_value
from erpnext.accounts.party import get_dashboard_info, get_default_contact
from erpnext.controllers.taxes_and_totals import get_itemised_tax_breakup_data
from frappe.model.base_document import _filter
import frappe


def format_phone(phone_number):
	"""
	Format a phone number in international format
	"""	
	if not phone_number:
		return ""

	try:
		formatted_phone = phone_number
		if not formatted_phone.startswith("+"):
			formatted_phone = "+91" + formatted_phone
		if is_valid_number(parse(formatted_phone)):
			return format_number(parse(formatted_phone), PhoneNumberFormat.INTERNATIONAL)
	except Exception as e:
		frappe.log_error(title=f"Failed to format phone {phone_number}", message=frappe.get_traceback(True))

	return phone_number


def get_contact(contact, fields=["*"]):
	if not contact:
		return None
	
	return frappe.get_all("Contact", filters={"name": contact}, fields=fields)[0]


def get_default_contact_detail(doctype, docname, fields=["*"]):
	contact = get_default_contact(doctype, docname)
	if contact:
		return get_contact(contact, fields=fields)


def get_company_logo(company, logo_field="company_logo"):
	return frappe.db.get_value("Company", company, logo_field)


def format_value(*args, **kwargs):
	return _format_value(*args, **kwargs)


def get_document(doctype, name):
	if doctype and name:
		return frappe.get_doc(doctype, name)


def get_document_amended_from_id(doctype, name):
	def get_amended_from(_name):
		p = frappe.db.get_value(doctype, _name, "amended_from")
		if not p:
			return _name
		return get_amended_from(p)

	return get_amended_from(name)


def get_customer_total_outstanding(customer):
	total_oustanding = 0
	for data in get_dashboard_info("Customer", customer):
		total_oustanding += data.get("total_unpaid") or 0
	return total_oustanding


def get_gst_rate_wise_details(sales_invoice_doc):
	"""
	Return a dictionary with a key "is_igst" and a list "gst_breakup".
	"gst_breakup" is a list of dictionaries, each dictionary contains tax rate and its corresponding CGST, SGST, IGST amounts.
	
	Example:
	{
		"is_igst": False,
		"gst_breakup": [
			{
				"tax_rate": 18, "taxable_amount": 0, "cgst_rate": 9, "cgst_amount": 0, "sgst_rate": 9, "sgst_amount": 0, "igst_rate": 0, "igst_amount": 0
			},
			{
				"tax_rate": 12, "taxable_amount": 0, "cgst_rate": 6, "cgst_amount": 0, "sgst_rate": 6, "sgst_amount": 0, "igst_rate": 0, "igst_amount": 0
			}
		]
	}
	"""

	if not sales_invoice_doc.taxes:
		return {
			"is_igst": False,
			"gst_breakup": []
		}
	
	tax_accounts = {}
	is_igst = False
	for tax in sales_invoice_doc.taxes:
		if getattr(tax, "category", None) and tax.category == "Valuation":
			continue

		if tax.gst_tax_type and tax.gst_tax_type not in tax_accounts:
			tax_accounts[tax.description] = tax.gst_tax_type
	
	itemised_tax_data = get_itemised_tax_breakup_data(sales_invoice_doc)

	tax_rate_wise_details = {}
	for row in itemised_tax_data:
		tax_rate = 0
		tax_detail = {
			"cgst_rate": 0,
			"cgst_amount": 0,
			"sgst_rate": 0,
			"sgst_amount": 0,
			"igst_rate": 0,
			"igst_amount": 0
		}

		for tax_desc, tax_type in tax_accounts.items():
			tax_account_detail = row.get(tax_desc)

			if tax_account_detail and tax_account_detail.get("tax_rate"):
				tax_rate += tax_account_detail.get("tax_rate")
				tax_detail[f"{tax_type}_rate"] = tax_account_detail.get("tax_rate")
				tax_detail[f"{tax_type}_amount"] = (tax_detail.get(f"{tax_type}_amount") or 0) + tax_account_detail.get("tax_amount")
		
		if not tax_rate:
			continue

		if tax_rate not in tax_rate_wise_details:
			tax_rate_wise_details[tax_rate] = frappe._dict({
				"tax_rate": tax_rate,
				"taxable_amount": row.get("taxable_amount") or 0,
				**tax_detail
			})
		else:
			tax_rate_wise_details[tax_rate].taxable_amount += row.get("taxable_amount") or 0
			
			for key, value in tax_detail.items():
				if key.endswith("_amount"):
					tax_rate_wise_details[tax_rate][key] = (tax_rate_wise_details[tax_rate].get(key) or 0) + value
		
		if tax_rate_wise_details[tax_rate]["igst_rate"]:
			is_igst = True

	return frappe._dict({
		"is_igst": is_igst,
		"gst_breakup": sorted(list(tax_rate_wise_details.values()), key=lambda x: x.tax_rate)
	})


def get_sales_invoice_serial_no_list(doc):
	serial_no_list = []
	idx = 0

	serial_batch_bundle_list = [d.serial_and_batch_bundle for d in doc.items if d.serial_and_batch_bundle]
	if not serial_batch_bundle_list:
		return []
	
	serial_list = frappe.get_all("Serial and Batch Entry", filters={
		"docstatus": 1,
		"parent": ["in", serial_batch_bundle_list]
	}, fields=["serial_no", "parent"], order_by="creation asc, idx asc")


	def get_dict(serial_no, _idx):
		return frappe._dict({
			"idx": _idx,
			"item_code": item.item_code,
			"item_name": item.item_name,
			"serial_no": serial_no
		})
	
	for item in doc.items:
		if not item.serial_and_batch_bundle:
			continue

		row_serial_no_list = _filter(serial_list, {
			"parent": item.serial_and_batch_bundle
		})

		for serial_no in row_serial_no_list:
			idx += 1
			serial_no_list.append(get_dict(serial_no.serial_no, idx))


	return serial_no_list


def extract_numeric_suffix(docname):
	"""
	Extracts and returns the numeric suffix from the provided docname.
	"""
	res = ""

	if docname:
		for char in docname[::-1]:
			if char.isdigit():
				res = char + res
			else:
				break

	return res
