// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.provide("erpnext.utils");

frappe.query_reports["Receivable Outstanding Report"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			reqd: 1,
			default: frappe.defaults.get_user_default("Company"),
		},
		{
			fieldname: "report_date",
			label: __("Posting Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
		},
		{
			fieldname: "party_type",
			label: __("Party Type"),
			fieldtype: "Autocomplete",
			options: get_party_type_options(),
			on_change: function () {
				frappe.query_report.set_filter_value("party", "");
				frappe.query_report.toggle_filter_display(
					"customer_group",
					frappe.query_report.get_filter_value("party_type") !== "Customer"
				);
			},
		},
		{
			fieldname: "party",
			label: __("Party"),
			fieldtype: "MultiSelectList",
			options: "party_type",
			get_data: function (txt) {
				if (!frappe.query_report.filters) return;

				let party_type = frappe.query_report.get_filter_value("party_type");
				if (!party_type) return;

				return frappe.db.get_link_options(party_type, txt);
			},
		},
		{
			fieldname: "ageing_based_on",
			label: __("Ageing Based On"),
			fieldtype: "Select",
			options: "Posting Date\nDue Date",
			default: "Due Date",
		},
		{
			fieldname: "range",
			label: __("Ageing Range"),
			fieldtype: "Data",
			default: "30, 60, 90, 120",
		},
		{
			fieldname: "payment_terms_template",
			label: __("Payment Terms Template"),
			fieldtype: "Link",
			options: "Payment Terms Template",
		},
		{
			fieldname: "custom_sales_person",
			label: __("Sales Person"),
			fieldtype: "MultiSelectList",
			get_data: function (txt) {
				return frappe.db.get_link_options("Sales Person", txt);
			}
		},
		{
			fieldname: "group_by_party",
			label: __("Group By Customer"),
			fieldtype: "Check",
		},
		{
			fieldname: "show_sales_person",
			label: __("Show Sales Person"),
			fieldtype: "Check",
		},
		{
			fieldname: "custom_invoice_type",
			label: __("Sales Type"),
			fieldtype: "MultiSelectList",
			options: ["CREDIT", "CASH", "COMMISSION"],
			default: []
		},
		{
			fieldname: "custom_sales_category",
			label: __("Sales Category"),
			fieldtype: "MultiSelectList",
			options: ["Product Sales", "Spare Sales", "Service Sales"],
			default: []
		},
	],

	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (data && data.bold) {
			value = value.bold();
		}
		return value;
	},

};

erpnext.utils.add_dimensions("Accounts Receivable", 9);

function get_party_type_options() {
	let options = [];
	frappe.db
		.get_list("Party Type", { filters: { account_type: "Receivable" }, fields: ["name"] })
		.then((res) => {
			res.forEach((party_type) => {
				options.push(party_type.name);
			});
		});
	return options;
}
