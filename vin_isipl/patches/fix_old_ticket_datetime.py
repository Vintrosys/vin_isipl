import frappe

def execute():
    if not frappe.db.table_exists("HD Ticket"):
        return

    tickets = frappe.get_all(
        "HD Ticket",
        fields=["name", "creation", "modified"]
    )
    for t in tickets:
        frappe.db.set_value(
            "HD Ticket",
            t.name,
            {
                "custom_created_on_date": t.creation.date(),
                "custom_created_on_time": t.creation.time().replace(microsecond=0),
                "custom_last_modified_date": t.modified.date(),
                "custom_last_modified_time": t.modified.time().replace(microsecond=0),
            },
            update_modified=False
        )
    frappe.db.commit()