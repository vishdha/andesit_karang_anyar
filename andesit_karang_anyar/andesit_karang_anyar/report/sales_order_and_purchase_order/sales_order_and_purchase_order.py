# Copyright (c) 2013, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
from frappe.utils import flt

def execute(filters=None):
	if not filters: filters = {}
    
	columns = get_columns(filters)
	entries = get_entries(filters)
	data = []
	total_wbt_net_weight = 0.0

	# To find Total of net weight at the end of report.
	if filters["doc_type"] == "Sales Order":
		for d in entries:
		#	total_wbt_net_weight += (d.wbt_net_weight)

			data.append([
				d.name, d.name, d.customer, d.company, d.transaction_date, d.delivery_date, d.shipping_address_name, d.grand_total, d.territory, d.customer_address,d.contact_person
			])
	elif filters["doc_type"] == "Purchase Order":
		for d in entries:
			data.append([
				d.name, d.name, d.supplier_name, d.company, d.transaction_date, d.supplier_address, d.grand_total, d.territory, d.supplier_address,d.contact_person
			])

	# if data:
	# 	total_row = [""]*len(data[0])
	# 	total_row[0] = _("Total")
	# 	total_row[-1] = total_wbt_net_weight
	# 	data.append(total_row)

	return columns, data
#Display Column row from Sales order.
def get_columns(filters):
	if not filters.get("doc_type"):
		msgprint(_("Please select the document type first"), raise_exception=1)

	if filters["doc_type"] == "Sales Order":
		return [filters["doc_type"] + ":Link/" + filters["doc_type"] + ":140",
			_("Customer") + ":Link/Customer:120",
			_("Customer Name") + ":Data:120",
			_("Company") + ":Link/Company:120",
			_("Date") + ":Date:120",
			_("Delivery Date") + ":Date:120",
			_("Shipping Address") + ":Link/DocType:120",
			_("Grand Total") + ":Float:160",
			_("Territory") + ":Link/Territory:160",
			_("Contact Address") + ":Link/Address:160",
			_("Contact Person") + ":Link/Contact:160"
		]
	elif filters["doc_type"] == "Purchase Order":
		return [filters["doc_type"] + ":Link/" + filters["doc_type"] + ":140",
			_("Supplier") + ":Link/Supplier:120",
			_("Supplier Name") + ":Data:120",
			_("Company") + ":Link/Company:120",
			_("Date") + ":Date:120",
			_("Supplier Address") + ":Link/DocType:120",
			_("Grand Total") + ":Float:160",
			_("Contact Address") + ":Link/Address:160",
			_("Contact Person") + ":Link/Contact:160"
		]


#Display Data in  Sales order and purchase order Report.
def get_entries(filters):
	if filters["doc_type"] == "Sales Order":
		entries = frappe.db.sql("""
			select
				cs.name, wt.name, wt.customer, wt.company, wt.transaction_date, wt.delivery_date,wt.shipping_address_name,wt.grand_total,wt.territory,wt.customer_address,wt.contact_person
			from 
				`tab%s` cs, `tabSales Order` wt 
			where 
				cs.name = wt.name
			""" %(filters["doc_type"]), as_dict=1)

	elif filters["doc_type"] == "Purchase Order":
		entries = frappe.db.sql("""
			select
				cs.name, wt.name, wt.supplier_name, wt.company, wt.transaction_date, wt.supplier_address,wt.grand_total,wt.supplier_address,wt.contact_person
			from 
				`tab%s` cs, `tabPurchase Order` wt 
			where 
				cs.name = wt.name	
			""" %(filters["doc_type"]), as_dict=1)


	return entries
