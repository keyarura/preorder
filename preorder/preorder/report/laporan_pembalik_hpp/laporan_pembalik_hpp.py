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
	sl_entries = frappe.db.sql("""select dn.`name`, dn.posting_date, dn.net_total, (select sum((actual_qty * -1) * valuation_rate) from `tabStock Ledger Entry` where voucher_no = dn.`name`) as hpp from `tabDelivery Note` dn where dn.docstatus = '1' %s and dn.is_return = '0' order by dn.`name` asc""" % conditions, as_dict=1)
	for ri in sl_entries:
		dn_date = ri.posting_date.strftime("%B %Y")
		count_inv = frappe.db.sql("""select count(distinct(si.`name`)) from `tabSales Invoice Item` sii inner join `tabSales Invoice` si on sii.parent = si.`name` where si.docstatus = '1' and sii.delivery_note = %s and si.type_of_invoice in ('Retention', 'Non Project Payment', 'Full Payment') and si.is_return = '0'""", ri.name)[0][0]
		count_si = frappe.db.sql("""select count(distinct(dni.against_sales_order)) from `tabDelivery Note Item` dni inner join `tabSales Invoice Item` sii on dni.against_sales_order = sii.sales_order inner join `tabSales Invoice` si on si.`name` = sii.parent where dni.parent = %s and si.docstatus = '1' and si.type_of_invoice in ('Retention', 'Non Project Payment', 'Full Payment')""", ri.name)[0][0]
		if count_inv != 0:
			si = frappe.db.sql("""select distinct(si.`name`) from `tabSales Invoice Item` sii inner join `tabSales Invoice` si on sii.parent = si.`name` where si.docstatus = '1' and sii.delivery_note = %s and si.type_of_invoice in ('Retention', 'Non Project Payment', 'Full Payment') and si.is_return = '0' limit 1""", ri.name)[0][0]
			invoice = frappe.db.get_value("Sales Invoice", si, ["posting_date", "net_total"], as_dict=1)
			si_date = invoice.posting_date.strftime("%B %Y")
			si_total = invoice.net_total
			count_jv = frappe.db.sql("""select count(*) from `tabJournal Entry` where docstatus = '1' and delivery_note = %s and reversing_entry = '0'""", ri.name)[0][0]
			count_jv2 = frappe.db.sql("""select count(*) from `tabJournal Entry` where docstatus = '1' and rss_sales_invoice = %s and reversing_entry = '0'""", si)[0][0]
			if count_jv != 0:
				je = frappe.db.get_value("Journal Entry", {"delivery_note": ri.name, "reversing_entry": 0, "docstatus": 1}, ["posting_date", "name"], as_dict=1)
				je_name = je.name
				je_date = je.posting_date
			elif count_jv2 != 0:
				je = frappe.db.get_value("Journal Entry", {"rss_sales_invoice": si, "reversing_entry": 0, "docstatus": 1}, ["posting_date", "name"], as_dict=1)
				je_name = je.name
				je_date = je.posting_date
			else:
				if dn_date == si_date:
					je_date = ""
				else:
					je_date = "<a href='/desk#Form/Journal%20Entry/New%20Journal%20Entry%201?delivery_note="+ri.name+"'>Make JV</a>"
				je_name = ""
			count_rj = frappe.db.sql("""select count(*) from `tabJournal Entry` where docstatus = '1' and delivery_note = %s and reversing_entry = '1'""", ri.name)[0][0]
			count_rj2 = frappe.db.sql("""select count(*) from `tabJournal Entry` where docstatus = '1' and rss_sales_invoice = %s and reversing_entry = '1'""", si)[0][0]
			if count_rj != 0:
				rj = frappe.db.get_value("Journal Entry", {"delivery_note": ri.name, "reversing_entry": 1, "docstatus": 1}, ["posting_date", "name"], as_dict=1)
				rj_date = rj.posting_date
				rj_name = rj.name
			elif count_rj2 != 0:
				rj = frappe.db.get_value("Journal Entry", {"rss_sales_invoice": si, "reversing_entry": 1, "docstatus": 1}, ["posting_date", "name"], as_dict=1)
				rj_date = rj.posting_date
				rj_name = rj.name
			else:
				rj_date = ""
				rj_name = ""
			if dn_date == si_date:
				check = "&#10004;"
			elif count_rj != 0:
				check = "&#10004;"
			elif count_rj2 != 0:
				check = "&#10004;"
			else:
				check ="-"
		elif count_si != 0:
			so = frappe.db.sql("""select distinct(dni.against_sales_order) from `tabDelivery Note Item` dni inner join `tabSales Invoice Item` sii on dni.against_sales_order = sii.sales_order inner join `tabSales Invoice` si on si.`name` = sii.parent where dni.parent = %s and si.docstatus = '1' and si.type_of_invoice in ('Retention', 'Non Project Payment', 'Full Payment') limit 1""", ri.name)[0][0]
			si = frappe.db.sql("""select distinct(si.`name`) from `tabSales Invoice` si inner join `tabSales Invoice Item` sii on si.`name` = sii.parent where si.docstatus = '1' and sii.sales_order = %s and si.type_of_invoice in ('Retention', 'Non Project Payment', 'Full Payment')""", so)[0][0]
			invoice = frappe.db.get_value("Sales Invoice", si, ["posting_date", "net_total"], as_dict=1)
			si_date = invoice.posting_date.strftime("%B %Y")
			si_total = invoice.net_total
			count_jv = frappe.db.sql("""select count(*) from `tabJournal Entry` where docstatus = '1' and delivery_note = %s and reversing_entry = '0'""", ri.name)[0][0]
			count_jv2 = frappe.db.sql("""select count(*) from `tabJournal Entry` where docstatus = '1' and rss_sales_invoice = %s and reversing_entry = '0'""", si)[0][0]
			if count_jv != 0:
				je = frappe.db.get_value("Journal Entry", {"delivery_note": ri.name, "reversing_entry": 0, "docstatus": 1}, ["posting_date", "name"], as_dict=1)
				je_name = je.name
				je_date = je.posting_date
			elif count_jv2 != 0:
				je = frappe.db.get_value("Journal Entry", {"rss_sales_invoice": si, "reversing_entry": 0, "docstatus": 1}, ["posting_date", "name"], as_dict=1)
				je_name = je.name
				je_date = je.posting_date
			else:
				if dn_date == si_date:
					je_date = ""
				else:
					je_date = "<a href='/desk#Form/Journal%20Entry/New%20Journal%20Entry%201?delivery_note="+ri.name+"'>Make JV</a>"
				je_name = ""
			count_rj = frappe.db.sql("""select count(*) from `tabJournal Entry` where docstatus = '1' and delivery_note = %s and reversing_entry = '1'""", ri.name)[0][0]
			count_rj2 = frappe.db.sql("""select count(*) from `tabJournal Entry` where docstatus = '1' and rss_sales_invoice = %s and reversing_entry = '1'""", si)[0][0]
			if count_rj != 0:
				rj = frappe.db.get_value("Journal Entry", {"delivery_note": ri.name, "reversing_entry": 1, "docstatus": 1}, ["posting_date", "name"], as_dict=1)
				rj_date = rj.posting_date
				rj_name = rj.name
			elif count_rj2 != 0:
				rj = frappe.db.get_value("Journal Entry", {"rss_sales_invoice": si, "reversing_entry": 1, "docstatus": 1}, ["posting_date", "name"], as_dict=1)
				rj_date = rj.posting_date
				rj_name = rj.name
			else:
				rj_date = ""
				rj_name = ""
			if dn_date == si_date:
				check = "&#10004;"
			elif count_rj != 0:
				check = "&#10004;"
			elif count_rj2 != 0:
				check = "&#10004;"
			else:
				check ="-"
		else:
			si = ""
			si_date = ""
			si_total = ""
			count_jv = frappe.db.sql("""select count(*) from `tabJournal Entry` where docstatus = '1' and delivery_note = %s and reversing_entry = '0'""", ri.name)[0][0]
			if flt(count_jv) != 0:
				je = frappe.db.get_value("Journal Entry", {"delivery_note": ri.name, "reversing_entry": 0, "docstatus": 1}, ["posting_date", "name"], as_dict=1)
				je_name = je.name
				je_date = je.posting_date
			else:
				je_date = "<a href='/desk#Form/Journal%20Entry/New%20Journal%20Entry%201?delivery_note="+ri.name+"'>Make JV</a>"
				je_name = ""
			count_rj = frappe.db.sql("""select count(*) from `tabJournal Entry` where docstatus = '1' and delivery_note = %s and reversing_entry = '1'""", ri.name)[0][0]
			if count_rj != 0:
				rj = frappe.db.get_value("Journal Entry", {"delivery_note": ri.name, "reversing_entry": 1, "docstatus": 1}, ["posting_date", "name"], as_dict=1)
				rj_date = rj.posting_date
				rj_name = rj.name
			else:
				rj_date = ""
				rj_name = ""
			check = "-"
		data.append([dn_date, ri.name, ri.net_total, ri.hpp, si_date, si, si_total, je_date, je_name, rj_date, rj_name, check])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("Tgl DN")+"::100",
		_("No DN")+":Link/Delivery Note:100",
		_("Nilai DN")+":Currency:100",
		_("HPP")+":Currency:100",
		_("Tgl SI")+"::100",
		_("No SI")+":Link/Sales Invoice:100",
		_("Nilai SI")+":Currency:100",
		_("Tgl JV")+"::100",
		_("No JV")+":Link/Journal Entry:100",
		_("Tgl RJV")+"::100",
		_("No RJV")+":Link/Journal Entry:100",
		_("Check")+"::50",
	]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += " and dn.posting_date <= '%s'" % frappe.db.escape(filters["from_date"])
	return conditions
