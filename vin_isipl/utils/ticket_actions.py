import frappe
from frappe.utils import time_diff_in_hours, now_datetime
from frappe import _
from vin_isipl.events.whatsapp_message import send_checkin_notification

@frappe.whitelist()
def checkout_and_compute(ticket):

    try:
        doc = frappe.get_doc("HD Ticket", ticket)

        now = now_datetime()
        doc.custom_check_out = now

        if doc.custom_check_in:            
            hours = time_diff_in_hours(doc.custom_check_out, doc.custom_check_in)
            doc.custom_time_spent = round(hours, 2)
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        return {
            "check_out": doc.custom_check_out,
            "time_spent": doc.custom_time_spent
        }
    
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "CheckOut Error")
        frappe.throw("Failed to check out: " + str(e))


@frappe.whitelist()
def set_check_in(ticket):
    try :
        doc = frappe.get_doc("HD Ticket", ticket)
        now = now_datetime()   
        doc.custom_check_in = now
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        # send_checkin_notification(doc)
        return {
            "check_in": str(now)
        }
    
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "CheckIn Error")
        frappe.throw("Failed to check in: " + str(e))

def validate(doc, method):
    old_doc = doc.get_doc_before_save()
    if old_doc.status == doc.status:
        return
    if doc.status == "Pending" and not doc.custom_pending_reason:
        frappe.throw("Please provide the Pending Reason")

    if doc.custom_pending_reason and not old_doc.custom_pending_reason:
        doc.status = "Pending"

    if doc.status == "Working":
        send_checkin_notification(doc)
    if doc.status == "Resolved":
        attachments = frappe.get_all(
            "File",
            filters={
                "attached_to_doctype": doc.doctype,
                "attached_to_name": doc.name
            },
            fields=["name"]
        )

        if not attachments:
            frappe.throw("Please attach a Service Report in the comments section")

    if not doc.is_new():        
        if old_doc and old_doc.status == "Resolved" and doc.status != "Resolved":
            frappe.throw("Status cannot be changed once Resolved")
    



