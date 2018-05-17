// Copyright (c) 2016, ridhosribumi and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Stock Available"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company"
		},
		{
			"fieldname":"warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse"
		},
		{
			"fieldname":"item_code",
			"label": __("Item"),
			"fieldtype": "Link",
			"options": "Item"
		},
		{
			"fieldname":"brand",
			"label": __("Brand"),
			"fieldtype": "Link",
			"options": "Brand"
		}

	],
	"formatter":function (row, cell, value, columnDef, dataContext, default_formatter) {
						value = default_formatter(row, cell, value, columnDef, dataContext);
						if (columnDef.id == "Warehouse_Stock") {
										if(dataContext.Warehouse_Stock != 0){
												value = "<div class='p-3 mb-2 bg-danger text-white'>" + value + "</div>";
										}
						}

						if (columnDef.id == "Planned_Qty") {
										if(dataContext.Planned_Qty != 0){
												value = "<div class='p-3 mb-2 bg-danger text-white'>" + value + "</div>";
										}
						}

						if (columnDef.id == "Requested_Qty") {
										if(dataContext.Requested_Qty != 0){
												value = "<div class='p-3 mb-2 bg-danger text-white'>" + value + "</div>";
										}
						}

						if (columnDef.id == "Indent_Qty") {
										if(dataContext.Indent_Qty != 0){
												value = "<div class='p-3 mb-2 bg-danger text-white'>" + value + "</div>";
										}
						}

						if (columnDef.id == "Booking_Qty") {
										if(dataContext.Booking_Qty != 0){
												value = "<div class='p-3 mb-2 bg-danger text-white'>" + value + "</div>";
										}
						}

						if (columnDef.id == "Reserved_Qty_for_Production") {
										if(dataContext.Reserved_Qty_for_Production != 0){
												value = "<div class='p-3 mb-2 bg-danger text-white'>" + value + "</div>";
										}
						}

						if (columnDef.id == "Available_Qty") {
										if(dataContext.Available_Qty != 0){
												value = "<div class='p-3 mb-2 bg-danger text-white'>" + value + "</div>";
										}
						}

						if (columnDef.id == "Reorder_Level") {
										if(dataContext.Reorder_Level != 0){
												value = "<div class='p-3 mb-2 bg-danger text-white'>" + value + "</div>";
										}
						}

						if (columnDef.id == "Reorder_Qty") {
										if(dataContext.Reorder_Qty != 0){
												value = "<div class='p-3 mb-2 bg-danger text-white'>" + value + "</div>";
										}
						}

						if (columnDef.id == "Shortage_Qty") {
										if(dataContext.Shortage_Qty != 0){
												value = "<div class='p-3 mb-2 bg-danger text-white'>" + value + "</div>";
										}
						}

						return value;
				}
}
