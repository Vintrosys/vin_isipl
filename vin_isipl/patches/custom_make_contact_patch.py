
import frappe
from erpnext.selling.doctype.customer import customer

def custom_make_contact(args, is_primary_contact=1):

    values = {
        "doctype": "Contact",
        "is_primary_contact": is_primary_contact,
        "links": [{"link_doctype": args.get("doctype"), "link_name": args.get("name")}],
    }

    party_type = args.customer_type if args.doctype == "Customer" else args.supplier_type
    party_name_key = "customer_name" if args.doctype == "Customer" else "supplier_name"

    if party_type == "Individual":
        first, middle, last = customer.parse_full_name(args.get(party_name_key))
        values.update({
            "first_name": first,
            "middle_name": middle,
            "last_name": last,
        })
    else:
        values.update({
            "first_name": args.custom_contact_person_name,
            "company_name": args.get(party_name_key),
        })

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
