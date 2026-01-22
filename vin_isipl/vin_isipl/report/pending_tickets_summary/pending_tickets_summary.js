// Copyright (c) 2026, Vintrosys and contributors
// For license information, please see license.txt

frappe.query_reports["Pending Tickets Summary"] = {
	"filters": [
		 {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            width: 100
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            width: 100
        },
        {
            fieldname: "team",
            label: __("Team"),
            fieldtype: "Link",
            options: "HD Team",
            width: 120
        }
	]
};
