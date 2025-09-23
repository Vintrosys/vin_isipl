import frappe
from vin_isipl.events.whatsapp import send_whynoo_template

def on_ticket_created(doc, method):
    """
    Send Whatsapp Notification when a ticket is created
    """

    try:
        phone = doc.custom_mobile_number

        if not phone:
            frappe.log_error(message="No phone number provided for ticket {}".format(doc.name), title="Phone Number Unavailable")
            return

        phone_with_code = f"91{phone}"

        creation_template = frappe.db.get_single_value("Whynoo Settings", "ticket_creation")

        send_whynoo_template(
            phone_with_code,
            creation_template,  
            [doc.name]
        )
       
    except Exception as e:
        frappe.log_error(title="WhyNoo Ticket Creation Error", message=(frappe.get_traceback() or "") [:4000])


def on_ticket_update(doc, method):
    """
    Send Whatsapp Notification when 
    Ticket is Pending
    Ticket is Resolved
    """
    try:

        previous_doc = doc.get_doc_before_save()
        if not previous_doc:
            return  
        old_status = previous_doc.status
        old_reason = previous_doc.custom_pending_reason

        if old_status == doc.status and old_reason == doc.custom_pending_reason:
            return
        
        assigned_to = frappe.db.get_value(
            "ToDo",
            {"reference_type": "HD Ticket", "reference_name": doc.name},
            "allocated_to"
        )

        agent_name = frappe.db.get_value("User", assigned_to, "full_name") or assigned_to

        phone = doc.custom_mobile_number

        if not phone:
            frappe.log_error(message="No phone number provided for ticket {}".format(doc.name), title="Phone Number Unavailable")
            return

        phone_with_code = "91" + str(phone)
        resolved_template = frappe.get_single("Whynoo Settings").ticket_resolved
        pending_template = frappe.get_single("Whynoo Settings").ticket_pending
            
        if doc.status == "Resolved":
            send_whynoo_template(
                phone_with_code,
                resolved_template,   
                [doc.name, agent_name]   
            )
                    
        elif doc.status == "Pending" and doc.custom_pending_reason:
            reason = frappe.db.get_value("HD Ticket Pending Reason", doc.custom_pending_reason, "pending_reason")
            send_whynoo_template(
                phone_with_code,
                pending_template,  
                [doc.name, reason]   
            )
            
    except Exception:
        frappe.log_error(title="WhyNoo Ticket Update Error", message=(frappe.get_traceback() or "") [:4000])
        

