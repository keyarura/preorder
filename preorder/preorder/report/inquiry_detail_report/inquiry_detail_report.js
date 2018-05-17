// Copyright (c) 2016, ridhosribumi and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Inquiry Detail Report"] = {
	"filters": [
		{
			"fieldname":"inquiry",
			"label": __("Inquiry"),
			"fieldtype": "Link",
			"options": "Inquiry",
		},
		{
			"fieldname":"type",
			"label": __("Type"),
			"fieldtype": "Select",
			"options": ["", "Request", "Request Flender", "Request Project", "Request Service", "Request BST", "Request Project BST"],
		},
		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
		},
		{
			"fieldname":"sales",
			"label": __("Sales"),
			"fieldtype": "Link",
			"options": "Sales Person",
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.month_start(frappe.datetime.get_today()),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
	]
}
