// Copyright (c) 2016, ridhosribumi and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Selling Progress Report"] = {
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
		},
	],
	"formatter":function (row, cell, value, columnDef, dataContext, default_formatter) {
						value = default_formatter(row, cell, value, columnDef, dataContext);
						if (columnDef.id == "StatusInquiry") {
										if(dataContext.StatusInquiry == "Completed"){
												value = "<div class='p-3 mb-2 bg-danger text-white'>" + value + "</div>";
										}else if(dataContext.StatusInquiry == "Submitted"){
												value = "<div class='p-3 mb-2 bg-primary text-white'>" + value + "</div>";
										}else  {
												value = "<div class='p-3 mb-2 bg-warning text-white'>" + value + "</div>";
										}
						}

						if (columnDef.id == "StatusQuotation") {
										if(dataContext.StatusQuotation == "Completed"){
												value = "<div class='p-3 mb-2 bg-danger text-white'>" + value + "</div>";
										}else if(dataContext.StatusQuotation == "Submitted"){
												value = "<div class='p-3 mb-2 bg-primary text-white'>" + value + "</div>";
										}else if(dataContext.StatusQuotation == "Partial SO"){
												value = "<div class='p-3 mb-2 bg-info text-white'>" + value + "</div>";
										}else  {
												value = "<div class='p-3 mb-2 bg-warning text-white'>" + value + "</div>";
										}
						}

						if (columnDef.id == "StatusSalesOrder") {
										if(dataContext.StatusSalesOrder == "Completed"){
												value = "<div class='p-3 mb-2 bg-danger text-white'>" + value + "</div>";
										}else if(dataContext.StatusSalesOrder == "To Deliver and Bill"){
												value = "<div class='p-3 mb-2 bg-warning text-white'>" + value + "</div>";
										}else if(dataContext.StatusSalesOrder == "To Bill"){
													value = "<div class='p-3 mb-2 bg-success text-white'>" + value + "</div>";
										}else  {
												value = "<div class='p-3 mb-2 bg-info text-white'>" + value + "</div>";
										}
						}

						if (columnDef.id == "StatusDeliveryNote") {
										if(dataContext.StatusDeliveryNote == "Completed"){
												value = "<div class='p-3 mb-2 bg-danger text-white'>" + value + "</div>";
										}else if(dataContext.StatusDeliveryNote == "To Bill"){
													value = "<div class='p-3 mb-2 bg-success text-white'>" + value + "</div>";
										}else  {
												value = "<div class='p-3 mb-2 bg-info text-white'>" + value + "</div>";
										}
						}

						if (columnDef.id == "StatusSalesInvoice") {
										if(dataContext.StatusSalesInvoice == "Paid"){
												value = "<div class='p-3 mb-2 bg-danger text-white'>" + value + "</div>";
										}else if(dataContext.StatusSalesInvoice == "Unpaid"){
													value = "<div class='p-3 mb-2 bg-success text-white'>" + value + "</div>";
										}else  {
												value = "<div class='p-3 mb-2 bg-info text-white'>" + value + "</div>";
										}
						}
						return value;
				}
}
