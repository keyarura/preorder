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

	query = frappe.db.sql("""select * from `tabRequest for Supplier Quotation` where docstatus = '1' %s order by `name` asc""" % conditions, as_dict=1)
	for si in query:
		items = frappe.db.sql("""select * from `tabRequest for Supplier Quotation Inquiry` where parent = %s order by idx asc""",si.name, as_dict=1)
		no = 0
		for row in items:
			no = flt(no) + 1
			if flt(no) == 1:
				rfsq = si.name
				date = si.transaction_date
				supplier_name = si.supplier_name
				status = si.action_status
				creation = si.creation
				owner = si.owner
				modified = si.modified
				modified_by = si.modified_by
			else:
				rfsq = ""
				date = ""
				status = ""
				supplier_name = ""
			data.append([rfsq, date, row.inquiry,supplier_name, status,row.transaction_date,creation,owner,modified,modified_by])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("ID")+":Link/Request for Supplier Quotation:100",
		_("Date")+":Date:100",
		_("Inquiry")+":Link/Inquiry:120",
		_("Supplier")+":Data:200",
		_("Action Status")+":Data:200",
		_("Inquiry Date")+":Date:100",
		_("Created Date") + ":Datetime:150",
		_("Created By") + ":Data:200",
		_("Modified Date") + ":Datetime:150",
		_("Modified By") + ":Data:200"
	]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += " and transaction_date >= '%s'" % frappe.db.escape(filters["from_date"])
	if filters.get("to_date"):
		conditions += " and transaction_date <= '%s'" % frappe.db.escape(filters["to_date"])
	if filters.get("inquiry"):
		conditions += " and `name` = '%s'" % frappe.db.escape(filters["inquiry"])
	return conditions
