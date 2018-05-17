// Copyright (c) 2016, ridhosribumi and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Purchase Order Report"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 1,
			"default": frappe.defaults.get_user_default("Company")
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": sys_defaults.year_start_date,
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		}
	],
	"formatter":function (row, cell, value, columnDef, dataContext, default_formatter) {
						value = default_formatter(row, cell, value, columnDef, dataContext);
						if (columnDef.id == "ItemStatus") {
										if(dataContext.ItemStatus == "Completed"){
												value = "<div class='p-3 mb-2 bg-danger text-white'>" + value + "</div>";
										}else if(dataContext.ItemStatus == "Clear"){
												value = "<div class='p-3 mb-2 bg-primary text-white'>" + value + "</div>";
										}else if(dataContext.ItemStatus == "Clarify"){
												value = "<div class='p-3 mb-2 bg-warning text-white'>" + value + "</div>";
										}else  {
											  value = "<div class='p-3 mb-2 bg-success text-white'>" + value + "</div>";
										}
						}
						if (columnDef.id == "Status") {
										if(dataContext.Status == "Full Received"){
												value = "<div class='p-3 mb-2 bg-danger text-white'>" + value + "</div>";
										}else if(dataContext.Status == "Partial Received"){
												value = "<div class='p-3 mb-2 bg-warning text-white'>" + value + "</div>";
										}else  {
											  value = "<div class='p-3 mb-2 bg-primary text-white'>" + value + "</div>";
										}
						}


						return value;
				}
}
