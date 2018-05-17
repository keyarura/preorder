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

	query = frappe.db.sql("""select `name`, `status`, urgency_level, inquiry_type, customer_name, contact_person, sales, creation, `owner`, modified, modified_by from `tabInquiry` where docstatus = '1' %s order by `name` asc""" % conditions, as_dict=1)
	for si in query:
		items = frappe.db.sql("""select `name`, item_description, qty, uom, reference from `tabInquiry Item` where parent = %s order by idx asc""",si.name, as_dict=1)
		no = 0
		for row in items:
			no = flt(no) + 1
			if flt(no) == 1:
				status = si.status
				urgency_level = si.urgency_level
				inquiry = si.name
				inquiry_type = si.inquiry_type
				customer_name = si.customer_name
				contact_person = si.contact_person
				sales = si.sales
				creation = si.creation
				owner = si.owner
				modified = si.modified
				modified_by = si.modified_by
			else:
				status = ""
				urgency_level = ""
				#inquiry = ""
				inquiry_type = ""
				#customer_name = ""
				#contact_person = ""
				#sales = ""
				creation = ""
				owner = ""
				modified = ""
				modified_by = ""
			count = frappe.db.sql("""select count(*) from `tabQuotation Item` where inquiry_item = %s and docstatus != '2'""", row.name)[0][0]
			if flt(count) != 0:
				quotation = frappe.db.sql("""select parent from `tabQuotation Item` where docstatus != '2' and inquiry_item = %s""", row.name)[0][0]
			else:
				quotation = ""
			data.append([status, urgency_level, inquiry, inquiry_type, customer_name, contact_person, sales, row.item_description, row.reference, row.qty, row.uom, quotation,creation,owner,modified,modified_by])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("Status")+"::90",
		_("Urgency Level")+"::90",
		_("Inquiry")+":Link/Inquiry:120",
		_("Type")+"::120",
		_("Customer Name")+"::250",
		_("Contact Person")+":Link/Contact:110",
		_("Sales")+":Link/Sales Person:110",
		_("Item Description")+"::170",
		_("Reference")+"::150",
		_("Qty")+":Float:60",
		_("UOM")+":Link/UOM:50",
		_("Quotation")+":Link/Quotation:110",
		_("Created Date") + ":Datetime:150",
		_("Created By") + ":Data:200",
		_("Modified Date") + ":Datetime:150",
		_("Modified By") + ":Data:200"

	]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("inquiry"):
		conditions += " and `name` = '%s'" % frappe.db.escape(filters["inquiry"])
	if filters.get("type"):
		conditions += " and inquiry_type = '%s'" % frappe.db.escape(filters["type"])
	if filters.get("customer"):
		conditions += " and customer = '%s'" % frappe.db.escape(filters["customer"])
	if filters.get("sales"):
		conditions += " and sales = '%s'" % frappe.db.escape(filters["sales"])
	if filters.get("from_date"):
		conditions += " and transaction_date >= '%s'" % frappe.db.escape(filters["from_date"])
	if filters.get("to_date"):
		conditions += " and transaction_date <= '%s'" % frappe.db.escape(filters["to_date"])
	return conditions
