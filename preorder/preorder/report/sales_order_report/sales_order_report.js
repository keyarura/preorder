// Copyright (c) 2016, ridhosribumi and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Order Report"] = {
	"filters": [
		{
			"fieldname":"warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse",
			"reqd": 1,
			"default": "VPI WAREHOUSE - VPI"
		},
	],

	"formatter":function (row, cell, value, columnDef, dataContext, default_formatter) {
						value = default_formatter(row, cell, value, columnDef, dataContext);
						if (columnDef.id == "PO Status") {
										if(dataContext["PO Status"] == "Completed"){
												value = "<div class='p-3 mb-2 bg-success text-white'>" + value + "</div>";
										}else if(dataContext["PO Status"] == "To Receive and Bill"){
												value = "<div class='p-3 mb-2 bg-warning text-white'>" + value + "</div>";
										}else  {
											  value = "<div class='p-3 mb-2 bg-danger text-white'>" + value + "</div>";
										}
						}

						if (columnDef.id == "Item Status") {
										if(dataContext["Item Status"] == "Completed"){
												value = "<div class='p-3 mb-2 bg-success text-white'>" + value + "</div>";
										}else if(dataContext["Item Status"] == "Clear"){
												value = "<div class='p-3 mb-2 bg-primary text-white'>" + value + "</div>";
										}else if(dataContext["Item Status"] == "Clarify"){
												value = "<div class='p-3 mb-2 bg-warning text-white'>" + value + "</div>";
										}else  {
											  value = "<div class='p-3 mb-2 bg-danger text-white'>" + value + "</div>";
										}
						}

						if (columnDef.id == "Status DP") {
										if(dataContext["Status DP"] == "Paid"){
												value = "<div class='p-3 mb-2 bg-success text-white'>" + value + "</div>";
										}else if(dataContext["Status DP"] == "Unpaid"){
												value = "<div class='p-3 mb-2 bg-orange text-white'>" + value + "</div>";
										}else  {
											  value = "<div class='p-3 mb-2 bg-danger text-white'>" + value + "</div>";
										}
						}

						return value;
				}
}
