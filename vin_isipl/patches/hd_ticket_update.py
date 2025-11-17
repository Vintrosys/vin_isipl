import frappe

def execute():
    # Safety check: skip patch if DocType table does not exist
    if not frappe.db.table_exists("HD Ticket"):
        return

    # Get all HD Ticket records where custom_created_date is NOT set
    tickets = frappe.get_all(
        "HD Ticket",
        fields=["name", "creation"],
        filters={"custom_created_date": ["is", "not set"]}
    )

    # Update custom_created_date for each ticket
    for ticket in tickets:
        frappe.db.set_value(
            "HD Ticket",
            ticket.name,
            "custom_created_date",
            ticket.creation,
            update_modified=False
        )
