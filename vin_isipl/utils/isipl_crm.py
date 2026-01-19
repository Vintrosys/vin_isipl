import frappe
from frappe import _
from frappe.utils import  get_url_to_list, get_url_to_form

@frappe.whitelist()
def get_quotation_url(crm_deal, organization):
	erpnext_crm_settings = frappe.get_single("ERPNext CRM Settings")
	if not erpnext_crm_settings.enabled:
		frappe.throw(_("ERPNext is not integrated with the CRM"))
	customer = frappe.db.get_value("Customer", {"crm_deal": crm_deal})
	if not customer:
			org = frappe.db.get_value("CRM Deal", crm_deal,'organization')
			deals = frappe.get_list("CRM Deal", {'organization': org})
			for deal in deals:
				customer = frappe.db.exists("Customer", {"crm_deal": deal['name']})
				if customer:
					break
	if not customer:
			doc = frappe.new_doc("Customer")
			doc.customer_name = org
			doc.insert()
			customer = org
	if not erpnext_crm_settings.is_erpnext_in_different_site:
		quotation_url = get_url_to_list("Quotation")
		deal_owner = frappe.db.get_value("CRM Deal",crm_deal,"deal_owner")
		emp_name = frappe.db.get_value("Employee",{"user_id":deal_owner})
		sales_person = frappe.db.get_value("Sales Person",{"employee":emp_name})
		return f"{quotation_url}/new?quotation_to=Customer&party_name={customer}&crm_deal={crm_deal}&company={erpnext_crm_settings.erpnext_company}&sales_person={sales_person}"
    
@frappe.whitelist()
def get_customer_link(crm_deal):
	erpnext_crm_settings = frappe.get_single("ERPNext CRM Settings")
	if not erpnext_crm_settings.enabled:
		frappe.throw(_("ERPNext is not integrated with the CRM"))

	if not erpnext_crm_settings.is_erpnext_in_different_site:
		customer = frappe.db.exists("Customer", {"crm_deal": crm_deal})
		if not customer:
			org = frappe.db.get_value("CRM Deal", crm_deal,'organization')
			deals = frappe.get_list("CRM Deal", {'organization': org})
			for deal in deals:
				customer = frappe.db.exists("Customer", {"crm_deal": deal['name']})
				if customer:
					break
		if not customer:
			doc = frappe.new_doc("Customer")
			doc.customer_name = org
			doc.insert()
			customer = org
		return get_url_to_form("Customer", customer) if customer else ""
	

@frappe.whitelist()
def create_org(doc,action):
	if not frappe.db.exists("CRM Organization", doc.name):
		org = frappe.new_doc("CRM Organization")
		org.organization_name = doc.name
		org.insert()
		frappe.db.commit()
	if not frappe.db.exists("HD Customer", doc.name):
		hd_customer = frappe.new_doc("HD Customer")
		hd_customer.customer_name = doc.name
		hd_customer.insert()
		frappe.db.commit()
