import frappe
from frappe.utils import get_datetime


def execute():
    # Latest comment time per Deal (using modified or creation)
    rows = frappe.db.sql("""
        SELECT
            c.reference_name AS deal,
            MAX(COALESCE(c.modified, c.creation)) AS last_comment_ts
        FROM `tabComment` c
        WHERE c.reference_doctype = 'CRM Deal'
          AND c.reference_name IS NOT NULL
        GROUP BY c.reference_name
    """, as_dict=True)

    count = 0
    for r in rows:
        deal_name = r.deal
        last_comment_ts = r.last_comment_ts
        if not deal_name or not last_comment_ts:
            continue

        # Get current Deal.modified
        deal_modified = frappe.db.get_value("CRM Deal", deal_name, "modified")

        # If comment time is newer, update Deal.modified
        if not deal_modified or get_datetime(last_comment_ts) > get_datetime(deal_modified):
            
            frappe.db.set_value(
                "CRM Deal",
                deal_name,
                "modified",
                last_comment_ts,
                update_modified=False
            )
            count += 1

    frappe.db.commit()