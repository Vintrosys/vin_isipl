# Copyright (c) 2026, Vintrosys and contributors
# For license information, please see license.txt

import frappe
from datetime import date

def get_columns():
    return [
        {
            "label": "Ticket ID",
            "fieldname": "ticket_id",
            "fieldtype": "Link",
            "options": "HD Ticket",
            "width": 120,
        },
        {
            "label": "Date",
            "fieldname": "date",
            "fieldtype": "Date",
            "width": 120,
        },
         {
            "label": "Customer",
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 150,
        },
        {
            "label": "Team",
            "fieldname": "team",
            "fieldtype": "Link",
            "options": "HD Team",
            "width": 120,
        },
        {
            "label": "Technician",
            "fieldname": "technician",
            "fieldtype": "Data",
            "width": 180,
        },
        {
            "label": "Reason",
            "fieldname": "reason",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "label": "Pending Days",
            "fieldname": "pending_days",
            "fieldtype": "Int",
            "width": 120,
        },
    ]


def execute(filters=None):
    columns = get_columns()
    data = []

    conditions = ["t.status IN ('Pending', 'Testing', 'Claim')"]
    values = {}

    # 📅 Date filters
    if filters.get("from_date"):
        conditions.append("t.custom_created_date >= %(from_date)s")
        values["from_date"] = filters["from_date"]

    if filters.get("to_date"):
        conditions.append("t.custom_created_date <= %(to_date)s")
        values["to_date"] = filters["to_date"]

    # 👥 Team filter
    if filters.get("team"):
        conditions.append("t.agent_group = %(team)s")
        values["team"] = filters["team"]

    # 👤 Agent filter
    if filters.get("agent"):
        conditions.append("""
            EXISTS (
                SELECT 1
                FROM `tabHD Agent` a
                WHERE a.name = %(agent)s
                  AND JSON_CONTAINS(t._assign, JSON_QUOTE(a.user))
            )
        """)
        values["agent"] = filters["agent"]

    query = f"""
        SELECT
            t.name AS ticket_id,
            t.customer,
            t.agent_group,
            t.custom_created_date,
            t.creation,
            r.pending_reason,
            t.custom_team_lead,
            t._assign,
            u.full_name
        FROM `tabHD Ticket` t
        LEFT JOIN `tabUser` u ON u.name = t.custom_team_lead
        LEFT JOIN `tabHD Ticket Pending Reason` r
            ON r.name = t.custom_pending_reason
        WHERE {" AND ".join(conditions)}
        ORDER BY t.name
    """

    tickets = frappe.db.sql(query, values, as_dict=True)

    for t in tickets:
        technician = "Unassigned"

        # 1️⃣ Assigned agent other than team lead
        agent = frappe.db.sql("""
            SELECT agent_name
            FROM `tabHD Agent`
            WHERE JSON_CONTAINS(%s, JSON_QUOTE(user))
              AND user != %s
            ORDER BY agent_name
            LIMIT 1
        """, (t._assign, t.custom_team_lead), as_dict=True)

        if agent:
            technician = agent[0]["agent_name"]

        # 2️⃣ Only team lead assigned
        elif t._assign and frappe.db.sql("""
            SELECT JSON_CONTAINS(%s, JSON_QUOTE(%s)) AND JSON_LENGTH(%s) = 1
        """, (t._assign, t.custom_team_lead, t._assign))[0][0]:
            technician = t.full_name

        pending_days = (date.today() - t.creation.date()).days

        data.append({
            "technician": technician,
            "ticket_id": t.ticket_id,
            "reason": t.pending_reason,
            "customer": t.customer,
            "team": t.agent_group,
            "date": t.custom_created_date,
            "pending_days": pending_days,
        })

    return columns, data
