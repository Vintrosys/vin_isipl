import frappe

def process_hd_comment(doc):

    if  doc.reference_name and doc.reference_doctype == "HD Ticket" and doc.comment_type == "Comment" and not doc.custom_hd_comment_id:
        hd_comment = frappe.get_doc({
            "doctype": "HD Ticket Comment",
            "reference_ticket": doc.reference_name,
            "commented_by": doc.comment_email or doc.owner,
            "content": doc.content
        }).insert(ignore_permissions=True)
        frappe.db.set_value("Comment", doc.name, "custom_hd_comment_id", hd_comment.name)
    if doc.custom_hd_comment_id:
        frappe.db.set_value("HD Ticket Comment",doc.custom_hd_comment_id,"content",doc.content)

def delete_hd_comment(doc,action):
    if doc.custom_hd_comment_id:
        frappe.delete_doc("HD Ticket Comment",doc.custom_hd_comment_id)

def on_comment_update(doc, method=None):
    process_hd_comment(doc)
