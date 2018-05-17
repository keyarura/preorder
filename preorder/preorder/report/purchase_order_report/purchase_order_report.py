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
	sl_entries = frappe.db.sql("""select `name`, supplier_name, transaction_date, payment, delivery_term, delivery_time, freight, ship_term, ship_to_by, supplier_confirm_po, etd_supplier, eta_vpi, currency from `tabPurchase Order` po where po.docstatus = '1' %s""" % conditions, as_dict=1)
	for cl in sl_entries:
		count = frappe.db.sql("""select count(*) from `tabPurchase Order Item` where parent = %s""", cl.name)[0][0]
		for q in range(0,count):
			i = flt(q)+1
			items = frappe.db.sql("""select `name` from `tabPurchase Order Item` where parent = %s order by idx asc limit %s,%s """, (cl.name, q, i))[0][0]
			so = frappe.db.sql("""select sales_order from `tabPurchase Order Item` where parent = %s order by idx asc limit %s,%s """, (cl.name, q, i))[0][0]
			if so != None:
				so_delivery_date = frappe.db.get_value("Sales Order", so, "delivery_date")
			else:
				so_delivery_date = ""
			det = frappe.db.get_value("Purchase Order Item", items, ["hs_code", "item_code", "description", "qty", "rate", "received_qty", "item_status"], as_dict=1)
			if det.received_qty == 0:
				status_oto = "Not yet Received"
			elif det.received_qty < det.qty:
				status_oto = "Partial Received"
			else:
				status_oto = "Full Received"
			if flt(q) == 0:
				data.append([cl.name, so, so_delivery_date, cl.supplier_name, det.hs_code, det.item_code, det.description, det.qty, cl.currency, det.rate,  det.item_status, status_oto, cl.transaction_date, cl.payment, cl.delivery_time, cl.delivery_term, cl.freight, cl.ship_term, cl.ship_to_by, cl.supplier_confirm_po, cl.etd_supplier, cl.eta_vpi])
			else:
				data.append([cl.name, so, so_delivery_date, cl.supplier_name, det.hs_code, det.item_code, det.description, det.qty, cl.currency, det.rate, det.item_status, status_oto, '', '', '', '', '', '', '', '', '', ''])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("Purchase Order")+":Link/Purchase Order:110",
		_("Sales Order")+":Link/Sales Order:110",
		_("Delivery Date")+":Date:90",
		_("Supplier Name")+"::150",
		_("HS Code")+"::100",
		_("Item Code")+":Link/Item:150",
		_("Description")+"::150",
		_("Qty")+":Float:60",
		_("Currency")+":Link/Currency:70",
		_("Price")+":Float:110",
		_("ItemStatus")+"::100",
		_("Status")+"::120",
		_("PO Date")+":Date:90",
		_("Payment Term")+"::150",
		_("Delivery Time")+"::150",
		_("Delivery Term")+"::150",
		_("Freight")+"::100",
		_("Ship Term")+"::100",
		_("Ship to/by")+"::100",
		_("Supplier Confirm PO")+"::150",
		_("ETD Supplier")+":Date:90",
		_("ETA VPI")+":Date:90",
	]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("company"):
		conditions += " and po.company >= '%s'" % frappe.db.escape(filters["company"])
	if filters.get("from_date"):
		conditions += " and po.transaction_date >= '%s'" % frappe.db.escape(filters["from_date"])
	if filters.get("to_date"):
		conditions += " and po.transaction_date <= '%s'" % frappe.db.escape(filters["to_date"])

	return conditions
