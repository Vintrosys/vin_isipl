import frappe
from erpnext.selling.doctype.customer import customer

def custom_make_contact(args, is_primary_contact=1):
    # Validate required field
    if not args.get("custom_contact_person_name"):
        frappe.throw("Please provide the Contact Person Name.")

    values = {
        "doctype": "Contact",
        "is_primary_contact": is_primary_contact,
        "links": [{"link_doctype": args.get("doctype"), "link_name": args.get("name")}],
        "first_name": args.get("custom_contact_person_name"),
        "company_name": args.get("customer_name") if args.doctype == "Customer" else args.get("supplier_name"),
    }

    contact = frappe.get_doc(values)

    if args.get("email_id"):
        contact.add_email(args.get("email_id"), is_primary=True)
    if args.get("mobile_no"):
        contact.add_phone(args.get("mobile_no"), is_primary_mobile_no=True)

    flags = args.get("flags", {})
    contact.insert(ignore_permissions=flags.get("ignore_permissions", False))

    return contact

def apply_monkey_patch():
    customer.make_contact = custom_make_contact
