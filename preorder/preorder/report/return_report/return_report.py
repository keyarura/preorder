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

	query = frappe.db.sql("""select `name`, receipt_type, issue_type, total_outgoing_value, total_incoming_value, customer_code, customer_nama, supplier_code, supplier_nama, sales_person from `tabStock Entry` where docstatus = '1' and purpose in ('Material Receipt', 'Material Issue') %s""" % conditions, as_dict=1)
	for se in query:
		if se.receipt_type == "Sales Return" or se.issue_type == "Purchase Return" or se.receipt_type == "Exchange of Purchase Return" or se.issue_type == "Exchange of Sales Return":
			if se.receipt_type == "Sales Return" or se.receipt_type == "Exchange of Purchase Return":
				type_of_return = se.receipt_type
				return_amount = se.total_incoming_value
			else:
				type_of_return = se.issue_type
				return_amount = se.total_outgoing_value
			if se.customer_code:
				cs = se.customer_nama
			elif se.supplier_code:
				cs = se.supplier_nama
			else:
				cs = ""
			count_je = frappe.db.sql("""select count(*) from `tabJournal Entry` where docstatus = '1' and stock_entry = %s and voucher_type in ('Credit Note', 'Debit Note')""", se.name)[0][0]
			if count_je != 0:
				je = frappe.db.sql("""select `name` from `tabJournal Entry` where docstatus = '1' and stock_entry = %s and voucher_type in ('Credit Note', 'Debit Note') order by `name` asc limit 1""", se.name)[0][0]
				je_amount = frappe.db.get_value("Journal Entry", je, ["total_debit"])
				if se.receipt_type == "Sales Return" or se.receipt_type == "Exchange of Purchase Return":
					difference = flt(return_amount) - flt(je_amount)
				else:
					difference = flt(je_amount) - flt(return_amount)
			else:
				je = ""
				je_amount = ""
				if se.receipt_type == "Sales Return" or se.receipt_type == "Exchange of Purchase Return":
					difference = flt(return_amount)
				else:
					difference = 0 - flt(return_amount)
			data.append([se.name, cs, type_of_return, return_amount, je, je_amount, se.sales_person, difference])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("No Return")+":Link/Stock Entry:110",
		_("Customer/Supplier")+"::200",
		_("Return Type")+"::170",
		_("Return Amount")+":Currency:120",
		_("Debit/Credit Note")+":Link/Journal Entry:120",
		_("Debit/Credit Note Amount")+":Currency:160",
		_("Sales")+"::120",
		_("Difference")+":Currency:120"
	]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += " and posting_date >= '%s'" % frappe.db.escape(filters["from_date"])
	if filters.get("to_date"):
		conditions += " and posting_date <= '%s'" % frappe.db.escape(filters["to_date"])

	return conditions
