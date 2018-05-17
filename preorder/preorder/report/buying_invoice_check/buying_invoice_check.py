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
	sl_entries = frappe.db.sql("""select po.`name`, po.transaction_date, po.`status` as status_po from `tabPurchase Order` po where po.docstatus = '1' %s""" % conditions, as_dict=1)
	for cl in sl_entries:
		count_1 = frappe.db.sql("""select count(distinct(pi.`name`)) from `tabPurchase Invoice` pi inner join `tabPurchase Invoice Item` pii on pi.`name` = pii.parent where pi.docstatus != '2' and pii.purchase_order = %s and pi.type_of_invoice = 'Full Payment'""", cl.name)[0][0]
		count_2 = frappe.db.sql("""select count(distinct(pi.`name`)) from `tabPurchase Invoice Item` pii inner join `tabPurchase Invoice` pi on pi.`name` = pii.parent where pi.docstatus != '2' and pi.purchase_order = %s and pi.type_of_invoice = 'Down Payment'""", cl.name)[0][0]
		count_3 = frappe.db.sql("""select count(distinct(pi.`name`)) from `tabPurchase Invoice` pi inner join `tabPurchase Invoice Item` pii on pi.`name` = pii.parent where pi.docstatus != '2' and pii.purchase_order = %s and pi.type_of_invoice = 'Non Project Payment'""", cl.name)[0][0]
		count_4 = frappe.db.sql("""select count(distinct(pi.`name`)) from `tabPurchase Receipt` pr inner join `tabPurchase Receipt Item` pri on pr.`name` = pri.parent inner join `tabPurchase Invoice` pi on pr.`name` = pi.purchase_receipt where pi.docstatus != '2' and pi.type_of_invoice = 'Progress Payment' and pri.purchase_order = %s""", cl.name)[0][0]
		count_5 = frappe.db.sql("""select count(distinct(pi.`name`)) from `tabPurchase Invoice Item` pii inner join `tabPurchase Invoice` pi on pi.`name` = pii.parent where pi.docstatus != '2' and pi.purchase_order = %s and pi.type_of_invoice = 'Termin Payment'""", cl.name)[0][0]
		count_6 = frappe.db.sql("""select count(distinct(pi.`name`)) from `tabPurchase Invoice Item` pii inner join `tabPurchase Invoice` pi on pi.`name` = pii.parent where pi.docstatus != '2' and pii.purchase_order = %s and pi.type_of_invoice = 'Retention'""", cl.name)[0][0]
		if count_1 == 0 and count_2 == 0 and count_3 == 0 and count_4 == 0 and count_5 == 0 and count_6 == 0:
			count = 1
		else:
			if count_1 >= count_2 and count_1 >= count_3 and count_1 >= count_4 and count_1 >= count_5 and count_1 >= count_6:
				count = count_1
			elif count_2 >= count_1 and count_2 >= count_3 and count_2 >= count_4 and count_2 >= count_5 and count_2 >= count_6:
				count = count_2
			elif count_3 >= count_1 and count_3 >= count_2 and count_3 >= count_4 and count_3 >= count_5 and count_3 >= count_6:
				count = count_3
			elif count_4 >= count_1 and count_4 >= count_2 and count_4 >= count_3 and count_4 >= count_5 and count_4 >= count_6:
				count = count_4
			elif count_5 >= count_1 and count_5 >= count_2 and count_5 >= count_3 and count_5 >= count_4 and count_5 >= count_6:
				count = count_5
			else:
				count = count_6
		for q in range(0,count):
			i = flt(q)+1
			if q == 0:
				po_date = cl.transaction_date
				po_name = cl.name
				po_status = cl.status_po
			else:
				po_date = ""
				po_name = ""
				po_status = ""
			if flt(q) < flt(count_1):
				pi_1 = frappe.db.sql("""select distinct(pi.`name`) from `tabPurchase Invoice` pi inner join `tabPurchase Invoice Item` pii on pi.`name` = pii.parent where pi.docstatus != '2' and pii.purchase_order = %s and pi.type_of_invoice = 'Full Payment' order by pi.`name` asc limit %s,%s""", (cl.name, q, i))[0][0]
				pi_1_status = frappe.db.get_value("Purchase Invoice", pi_1, "status")
			else:
				pi_1 = ""
				pi_1_status = ""
			if flt(q) < flt(count_2):
				pi_2 = frappe.db.sql("""select distinct(pi.`name`) from `tabPurchase Invoice Item` pii inner join `tabPurchase Invoice` pi on pi.`name` = pii.parent where pi.docstatus != '2' and pi.purchase_order = %s and pi.type_of_invoice = 'Down Payment' order by pi.idx asc limit %s,%s""", (cl.name, q, i))[0][0]
				pi_2_status = frappe.db.get_value("Purchase Invoice", pi_2, "status")
			else:
				pi_2 = ""
				pi_2_status = ""
			if flt(q) < flt(count_3):
				pi_3 = frappe.db.sql("""select distinct(pi.`name`) from `tabPurchase Invoice` pi inner join `tabPurchase Invoice Item` pii on pi.`name` = pii.parent where pi.docstatus != '2' and pii.purchase_order = %s and pi.type_of_invoice = 'Non Project Payment' order by pi.`name` asc limit %s,%s""", (cl.name, q, i))[0][0]
				pi_3_status = frappe.db.get_value("Purchase Invoice", pi_3, "status")
			else:
				pi_3 = ""
				pi_3_status = ""
			if flt(q) < flt(count_4):
				pi_4 = frappe.db.sql("""select distinct(pi.`name`) from `tabPurchase Receipt` pr inner join `tabPurchase Receipt Item` pri on pr.`name` = pri.parent inner join `tabPurchase Invoice` pi on pr.`name` = pi.purchase_receipt where pi.docstatus != '2' and pi.type_of_invoice = 'Progress Payment' and pri.purchase_order = %s order by pi.`name` asc limit %s,%s""", (cl.name, q, i))[0][0]
				pi_4_status = frappe.db.get_value("Purchase Invoice", pi_4, "status")
			else:
				pi_4 = ""
				pi_4_status = ""
			if flt(q) < flt(count_5):
				pi_5 = frappe.db.sql("""select distinct(pi.`name`) from `tabPurchase Invoice Item` pii inner join `tabPurchase Invoice` pi on pi.`name` = pii.parent where pi.docstatus != '2' and pi.purchase_order = %s and pi.type_of_invoice = 'Termin Payment' order by pi.idx asc limit %s,%s""", (cl.name, q, i))[0][0]
				pi_5_status = frappe.db.get_value("Purchase Invoice", pi_5, "status")
			else:
				pi_5 = ""
				pi_5_status = ""
			if flt(q) < flt(count_6):
				pi_6 = frappe.db.sql("""select distinct(pi.`name`) from `tabPurchase Invoice Item` pii inner join `tabPurchase Invoice` pi on pi.`name` = pii.parent where pi.docstatus != '2' and pi.purchase_order = %s and pi.type_of_invoice = 'Retention' order by pi.idx asc limit %s,%s""", (cl.name, q, i))[0][0]
				pi_6_status = frappe.db.get_value("Purchase Invoice", pi_6, "status")
			else:
				pi_6 = ""
				pi_6_status = ""
			data.append([po_date, po_name, po_status, pi_1, pi_1_status, pi_2, pi_2_status, pi_3, pi_3_status, pi_4, pi_4_status, pi_5, pi_5_status, pi_6, pi_6_status])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("PO Date")+":Date:90",
		_("Purchase Order")+":Link/Purchase Order:110",
		_("Status")+":Data:130",
		_("Full Payment")+":Link/Purchase Invoice:110",
		_("Status 1")+":Data:90",
		_("Down Payment")+":Link/Purchase Invoice:110",
		_("Status 2")+":Data:90",
		_("Non Project Payment")+":Link/Purchase Invoice:130",
		_("Status 3")+":Data:90",
		_("Progress Payment")+":Link/Purchase Invoice:110",
		_("Status 4")+":Data:90",
		_("Termin Payment")+":Link/Purchase Invoice:110",
		_("Status 5")+":Data:90",
		_("Retention")+":Link/Purchase Invoice:110",
		_("Status 6")+":Data:90",
	]
	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += " and po.transaction_date >= '%s'" % frappe.db.escape(filters["from_date"])
	if filters.get("to_date"):
		conditions += " and po.transaction_date <= '%s'" % frappe.db.escape(filters["to_date"])
	if filters.get("need_down_payment") == 1:
		conditions += " and po.need_down_payment = '1'"
	return conditions
