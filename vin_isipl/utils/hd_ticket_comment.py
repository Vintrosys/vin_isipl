import frappe

def process_hd_comment(doc):

    if doc.reference_doctype != "HD Ticket" or doc.comment_type != "Comment":
        return

    if frappe.flags.in_hd_comment_update:
        return

    frappe.flags.in_hd_comment_update = True

    # Build HTML
    html_rows = []
    ticket = frappe.get_doc("HD Ticket", doc.reference_name)

    for row in ticket.custom_machine_type_list:
        html_rows.append(
            f'''
            <li data-list="ordered">
                <span class="ql-ui" contenteditable="false"></span>
                <span style="color: rgb(0, 102, 204);">{row.machine_name}</span>
            </li>
            '''
        )

    final_html = f'''
    <div class="ql-editor read-mode">
        <ol>
            {''.join(html_rows)}
        </ol>
    </div>
    '''

    # Update comment content
    frappe.db.set_value("Comment", doc.name, "content", final_html)

    # ------------------------------------
    # FIX: Get linked HD Ticket Comment
    # ------------------------------------
    existing_hd_comment_id = doc.get("custom_hd_comment_id")

    if existing_hd_comment_id:
        # Update existing
        frappe.db.set_value("HD Ticket Comment", existing_hd_comment_id, "content", final_html)

    else:
        # Create new only once
        hd_comment = frappe.get_doc({
            "doctype": "HD Ticket Comment",
            "reference_ticket": doc.reference_name,
            "comment_id": doc.name,  # Only if field exists
            "commented_by": doc.comment_email or doc.owner,
            "content": final_html
        }).insert(ignore_permissions=True)

        # Save link back
        frappe.db.set_value("Comment", doc.name, "custom_hd_comment_id", hd_comment.name)

    frappe.flags.in_hd_comment_update = False


def on_comment_insert(doc, method=None):
    process_hd_comment(doc)


def on_comment_update(doc, method=None):
    process_hd_comment(doc)
