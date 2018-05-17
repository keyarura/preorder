# Copyright (c) 2013, ridhosribumi and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, getdate

def execute(filters=None):
	columns = get_columns()
#	sl_entries = get_entries(filters)
	data = []
	conditions = get_conditions(filters)

	sl_entries = frappe.db.sql("""select si.`name`, si.posting_date, si.net_total from `tabSales Invoice` si where si.docstatus = '1' and si.type_of_invoice in ('Retention', 'Non Project Payment', 'Full Payment') and si.`status` = 'Paid' and si.tt_advanced = '0' %s""" % conditions, as_dict=1)
	for cl in sl_entries:
		count_1 = frappe.db.sql("""select count(*) from `tabPayment Entry Reference` where reference_name = %s and docstatus = '1'""", cl.name)[0][0]
		if count_1 == 0:
			count = 1
		else:
			count = count_1
		for q in range(0,count):
			i = flt(q)+1
			if q == 0:
				si_name = cl.name
				si_date = cl.posting_date
				si_amount = cl.net_total
				c1 = frappe.db.sql("""select so_detail, dn_detail from `tabSales Invoice Item` where docstatus = '1' and parent = %s""", cl.name, as_dict=1)
				cogs = 0
				for c2 in c1:
					if c2.dn_detail:
						c6 = frappe.db.sql("""select sum((actual_qty * -1) * valuation_rate) from `tabStock Ledger Entry` where voucher_detail_no = %s""", c2.dn_detail)[0][0]
						cogs = flt(cogs) + flt(c6)
					else:
						c3 = frappe.db.sql("""select count(*) from `tabDelivery Note Item` where docstatus = '1' and so_detail = %s""", c2.so_detail)[0][0]
						if flt(c3) != 0:
							c4 = frappe.db.sql("""select `name` from `tabDelivery Note Item` where docstatus = '1' and so_detail = %s""", c2.so_detail, as_dict=1)
							for c5 in c4:
								c6 = frappe.db.sql("""select sum((actual_qty * -1) * valuation_rate) from `tabStock Ledger Entry` where voucher_detail_no = %s""", c5.name)[0][0]
								cogs = flt(cogs) + flt(c6)
						else:
							cogs = flt(cogs)
				count_2 = frappe.db.sql("""select count(distinct(inquiry)) from `tabSales Invoice Item` where parent = %s""", cl.name)[0][0]
				if count_2 != 0:
					inquiry = frappe.db.sql("""select distinct(inquiry) from `tabSales Invoice Item` where parent = %s and inquiry is not null""", cl.name, as_dict=1)
					expenses = 0
					for inq in inquiry:
						total_from_inquiry = frappe.db.get_value("Inquiry", inq.inquiry, ["total_invoice", "total_expense"], as_dict=1)
						item_amount = frappe.db.sql("""select sum(amount) from `tabSales Invoice Item` where docstatus = '1' and inquiry = %s and parent = %s""", (inq.inquiry, cl.name))[0][0]
						if flt(item_amount) != 0 and flt(total_from_inquiry.total_expense) != 0 and flt(total_from_inquiry.total_invoice) != 0:
							expense = flt(item_amount) * flt(total_from_inquiry.total_expense) / flt(total_from_inquiry.total_invoice)
						else:
							expense = 0
						expenses = flt(expenses) + flt(expense)
				else:
					expenses = 0
				net_profit = ""
				net_profit = flt(si_amount) - (flt(cogs) + flt(expenses))
			else:
				si_name = ""
				si_date = ""
				si_amount = ""
				cogs = ""
				expenses = ""
				net_profit = ""
			if flt(q) < flt(count_1):
				payment = frappe.db.sql("""select parent from `tabPayment Entry Reference` where reference_name = %s and docstatus = '1' order by parent asc limit %s,%s""", (cl.name, q, i))[0][0]
				payment_date = frappe.db.sql("""select posting_date from `tabPayment Entry` where `name` = %s""", payment)[0][0]
			else:
				payment = ""
				payment_date = ""
			data.append([si_name, si_date, si_amount, payment, payment_date, cogs, expenses, net_profit])

	# Untuk TT Advanced
	sl_entries = frappe.db.sql("""select distinct(si.`name`), si.posting_date, si.net_total from `tabSales Invoice` si inner join `tabSales Invoice Item` sii on si.`name` = sii.parent inner join `tabDelivery Note Item` dni on dni.against_sales_order = sii.sales_order inner join `tabDelivery Note` dn on dn.`name` = dni.parent where si.docstatus = '1' and si.type_of_invoice in ('Retention', 'Non Project Payment', 'Full Payment') and si.`status` = 'Paid' and si.tt_advanced = '1' and dn.docstatus = '1' and si.company = %s and dn.posting_date >= %s and dn.posting_date <= %s""", (frappe.db.escape(filters.get("company")), frappe.db.escape(filters.get("from_date")), frappe.db.escape(filters.get("to_date"))), as_dict=1)
	for cl in sl_entries:
		count_1 = frappe.db.sql("""select count(*) from `tabPayment Entry Reference` where reference_name = %s and docstatus = '1'""", cl.name)[0][0]
		if count_1 == 0:
			count = 1
		else:
			count = count_1
		for q in range(0,count):
			i = flt(q)+1
			if q == 0:
				si_name = cl.name
				si_date = cl.posting_date
				si_amount = cl.net_total
				c1 = frappe.db.sql("""select so_detail, dn_detail from `tabSales Invoice Item` where docstatus = '1' and parent = %s""", cl.name, as_dict=1)
				cogs = 0
				for c2 in c1:
					if c2.dn_detail:
						c6 = frappe.db.sql("""select sum((actual_qty * -1) * valuation_rate) from `tabStock Ledger Entry` where voucher_detail_no = %s""", c2.dn_detail)[0][0]
						cogs = flt(cogs) + flt(c6)
					else:
						c3 = frappe.db.sql("""select count(*) from `tabDelivery Note Item` where docstatus = '1' and so_detail = %s""", c2.so_detail)[0][0]
						if flt(c3) != 0:
							c4 = frappe.db.sql("""select `name` from `tabDelivery Note Item` where docstatus = '1' and so_detail = %s""", c2.so_detail, as_dict=1)
							for c5 in c4:
								c6 = frappe.db.sql("""select sum((actual_qty * -1) * valuation_rate) from `tabStock Ledger Entry` where voucher_detail_no = %s""", c5.name)[0][0]
								cogs = flt(cogs) + flt(c6)
						else:
							cogs = flt(cogs)
				count_2 = frappe.db.sql("""select count(distinct(inquiry)) from `tabSales Invoice Item` where parent = %s""", cl.name)[0][0]
				if count_2 != 0:
					inquiry = frappe.db.sql("""select distinct(inquiry) from `tabSales Invoice Item` where parent = %s and inquiry is not null""", cl.name, as_dict=1)
					expenses = 0
					for inq in inquiry:
						total_from_inquiry = frappe.db.get_value("Inquiry", inq.inquiry, ["total_invoice", "total_expense"], as_dict=1)
						item_amount = frappe.db.sql("""select sum(amount) from `tabSales Invoice Item` where docstatus = '1' and inquiry = %s and parent = %s""", (inq.inquiry, cl.name))[0][0]
						if flt(item_amount) != 0 and flt(total_from_inquiry.total_expense) != 0 and flt(total_from_inquiry.total_invoice) != 0:
							expense = flt(item_amount) * flt(total_from_inquiry.total_expense) / flt(total_from_inquiry.total_invoice)
						else:
							expense = 0
						expenses = flt(expenses) + flt(expense)
				else:
					expenses = 0
				net_profit = ""
				net_profit = flt(si_amount) - (flt(cogs) + flt(expenses))
			else:
				si_name = ""
				si_date = ""
				si_amount = ""
				cogs = ""
				expenses = ""
				net_profit = ""
			if flt(q) < flt(count_1):
				payment = frappe.db.sql("""select parent from `tabPayment Entry Reference` where reference_name = %s and docstatus = '1' order by parent asc limit %s,%s""", (cl.name, q, i))[0][0]
				payment_date = frappe.db.sql("""select posting_date from `tabPayment Entry` where `name` = %s""", payment)[0][0]
			else:
				payment = ""
				payment_date = ""
			data.append([si_name, si_date, si_amount, payment, payment_date, cogs, expenses, net_profit])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("Sales Invoice")+":Link/Sales Invoice:120",
		_("Posting Date")+":Date:100",
		_("Selling Amount")+":Currency:120",
		_("Payment")+":Link/Payment Entry:120",
		_("Payment Date")+":Date:120",
		_("HPP")+":Float:120",
		_("Expenses")+":Float:120",
		_("Net Profit")+":Float:120",
	]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("company"):
		conditions += " and si.company = '%s'" % frappe.db.escape(filters["company"])
	if filters.get("from_date"):
		conditions += " and si.paid_date >= '%s'" % frappe.db.escape(filters["from_date"])
	if filters.get("to_date"):
		conditions += " and si.paid_date <= '%s'" % frappe.db.escape(filters["to_date"])

	return conditions
