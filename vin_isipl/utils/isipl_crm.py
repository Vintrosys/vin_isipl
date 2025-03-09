import frappe
from frappe import _
from frappe.utils import  get_url_to_list


@frappe.whitelist()
def get_quotation_url(crm_deal, organization):
    erpnext_crm_settings = frappe.get_single("ERPNext CRM Settings")
    if not erpnext_crm_settings.enabled:
        frappe.throw(_("ERPNext is not integrated with the CRM"))
    customer = frappe.db.get_value("Customer", {"crm_deal": crm_deal})
    if not erpnext_crm_settings.is_erpnext_in_different_site:
        quotation_url = get_url_to_list("Quotation")
        return f"{quotation_url}/new?quotation_to=Customer&party_name={customer}&company={erpnext_crm_settings.erpnext_company}"