# Copyright (c) 2013, ridhosribumi and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, getdate

def execute(filters=None):
	columns = get_columns()
	data = []
	conditions = get_conditions(filters)

	query = frappe.db.sql("""select si.`name` as invoice, si.customer_name, si.customer_group, si.posting_date, sii.item_code, sii.item_name, sii.item_group, sii.warehouse, sii.qty, sii.net_amount as selling_amount,  si.currency, sii.so_detail, sii.dn_detail from `tabSales Invoice Item` sii inner join `tabSales Invoice` si on si.`name` = sii.parent	where si.docstatus = '1' and si.tt_advanced = '0' and si.type_of_invoice in ('Retention', 'Non Project Payment', 'Full Payment') %s order by si.posting_date asc, si.`name` asc""" % conditions, as_dict=1)
	for si in query:
		if si.dn_detail:
			cogs = frappe.db.sql("""select sum((actual_qty * -1) * valuation_rate) from `tabStock Ledger Entry` where voucher_detail_no = %s""", si.dn_detail)[0][0]
		else:
			count_dni = frappe.db.sql("""select count(*) from `tabDelivery Note Item` where docstatus = '1' and so_detail = %s""", si.so_detail)[0][0]
			if flt(count_dni) != 0:
				query_dni = frappe.db.sql("""select `name` from `tabDelivery Note Item` where docstatus = '1' and so_detail = %s""", si.so_detail, as_dict=1)
				cogs = 0
				for dni in query_dni:
					sle = frappe.db.sql("""select sum((actual_qty * -1) * valuation_rate) from `tabStock Ledger Entry` where voucher_detail_no = %s""", dni.name)[0][0]
					cogs = flt(cogs) + flt(sle)
			else:
				cogs = 0
		gross_profit = flt(si.selling_amount) - flt(cogs)
		percentage = (flt(gross_profit) / flt(si.selling_amount)) * 100
		data.append([si.invoice, si.customer_name, si.customer_group, si.posting_date, si.item_code, si.item_name, si.item_group, si.warehouse, si.qty, si.selling_amount, cogs, gross_profit, percentage, si.currency])

	# Untuk TT Advanced
	query = frappe.db.sql("""select si.`name` as invoice, si.customer_name, si.customer_group, si.posting_date, sii.item_code, sii.item_name, sii.item_group, sii.warehouse, sii.qty, sii.net_amount as selling_amount,  si.currency, sii.so_detail, dni.`name` as dn_detail from `tabSales Invoice` si inner join `tabSales Invoice Item` sii on si.`name` = sii.parent inner join `tabDelivery Note Item` dni on sii.sales_order = dni.against_sales_order inner join `tabDelivery Note` dn on dni.parent = dn.`name`	where si.docstatus = '1' and dn.docstatus = '1' and si.tt_advanced = '1' and si.type_of_invoice in ('Retention', 'Non Project Payment', 'Full Payment') and si.company = %s and dn.posting_date >= %s and dn.posting_date <= %s order by si.posting_date asc, si.`name` asc""", (frappe.db.escape(filters.get("company")), frappe.db.escape(filters.get("from_date")), frappe.db.escape(filters.get("to_date"))), as_dict=1)
	for si in query:
		if si.dn_detail:
			cogs = frappe.db.sql("""select sum((actual_qty * -1) * valuation_rate) from `tabStock Ledger Entry` where voucher_detail_no = %s""", si.dn_detail)[0][0]
		else:
			count_dni = frappe.db.sql("""select count(*) from `tabDelivery Note Item` where docstatus = '1' and so_detail = %s""", si.so_detail)[0][0]
			if flt(count_dni) != 0:
				query_dni = frappe.db.sql("""select `name` from `tabDelivery Note Item` where docstatus = '1' and so_detail = %s""", si.so_detail, as_dict=1)
				cogs = 0
				for dni in query_dni:
					sle = frappe.db.sql("""select sum((actual_qty * -1) * valuation_rate) from `tabStock Ledger Entry` where voucher_detail_no = %s""", dni.name)[0][0]
					cogs = flt(cogs) + flt(sle)
			else:
				cogs = 0
		gross_profit = flt(si.selling_amount) - flt(cogs)
		percentage = (flt(gross_profit) / flt(si.selling_amount)) * 100
		data.append([si.invoice, si.customer_name, si.customer_group, si.posting_date, si.item_code, si.item_name, si.item_group, si.warehouse, si.qty, si.selling_amount, cogs, gross_profit, percentage, si.currency])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("Sales Invoice")+":Link/Sales Invoice:100",
		_("Customer Name")+"::150",
		_("Customer Group")+":Link/Customer Group:120",
		_("Posting Date")+":Date:90",
		_("Item Code")+":Link/Item:120",
		_("Item Name")+"::120",
		_("Item Group")+":Link/Item Group:120",
		_("Warehouse")+":Link/Warehouse:150",
		_("Qty")+":Float:50",
		_("Selling Amount")+":Float:110",
		_("COGS")+":Float:110",
		_("Gross Profit")+":Float:110",
		_("Gross Profit %")+":Float:90",
		_("Currency")+":Link/Currency:60",
	]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("company"):
		conditions += " and si.company = '%s'" % frappe.db.escape(filters["company"])
	if filters.get("from_date"):
		conditions += " and si.posting_date >= '%s'" % frappe.db.escape(filters["from_date"])
	if filters.get("to_date"):
		conditions += " and si.posting_date <= '%s'" % frappe.db.escape(filters["to_date"])
	return conditions
