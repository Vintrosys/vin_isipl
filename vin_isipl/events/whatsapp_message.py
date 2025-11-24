import frappe
from vin_isipl.events.whatsapp import send_whynoo_template
from frappe import _


def on_ticket_update(doc, method):
    """
    Send Whatsapp Notification when 
    Ticket is Open
    Ticket is Resolved
    """
    try:
        if doc.custom_machine_type_list:
            summary = []
            for row in doc.custom_machine_type_list:
                line = f"{row.machine_type}"
                summary.append(line)

            # Save output
            if summary:
                doc.custom_machine_details = ", ".join(summary)

        previous_doc = doc.get_doc_before_save()
        if not previous_doc:
            return  

        phone = doc.custom_mobile_number

        if not phone.isdigit() or not len(phone) ==10:
            frappe.throw(_("Please Enter Correct Contact No"))

        phone_with_code = "91"+str(phone)
        resolved_template = frappe.get_single("Whynoo Settings").ticket_resolved
        pending_template = frappe.get_single("Whynoo Settings").ticket_pending
        creation_template = frappe.db.get_single_value("Whynoo Settings", "ticket_creation")
        assigned_to = frappe.db.get_value("ToDo",
             {"reference_type": "HD Ticket", "reference_name": doc.name, "status":"Open"},"allocated_to")
        agent_name = frappe.db.get_value("User", assigned_to, "full_name") or assigned_to
        if previous_doc.custom_mobile_number != phone:
            send_whynoo_template(
                phone_with_code,
                creation_template,  
                [doc.name]
            )  

        if doc.status == "Resolved":
            send_whynoo_template(
                phone_with_code,
                resolved_template,   
                [doc.name, agent_name]   
            )
            
    except Exception:
        frappe.log_error(title="WhyNoo Ticket Update Error", message=(frappe.get_traceback() or "") [:4000])