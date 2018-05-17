// Copyright (c) 2017, ridhosribumi and contributors
// For license information, please see license.txt

frappe.ui.form.on('Product Assembly', {
	setup: function(frm) {
		frm.get_field('items').grid.editable_fields = [
			{fieldname: 'type', columns: 3},
			{fieldname: 'item_description', columns: 3},
			{fieldname: 'brand', columns: 2},
			{fieldname: 'qty', columns: 2},
			{fieldname: 'uom', columns: 2}
		];
	},
	refresh: function(frm) {
		if(frm.doc.docstatus == 1 && frm.doc.status == "Submitted") {
			cur_frm.add_custom_button(__('Product Bundle'), cur_frm.cscript['Product Bundle'], __("Make"));
			cur_frm.page.set_inner_btn_group_as_primary(__("Make"));
		}
	},
	get_item_from_product_bundle: function(frm){
		erpnext.utils.map_current_doc({
			method: "preorder.preorder.doctype.product_assembly.product_assembly.get_items_product_bundle",
			source_name: frm.doc.product_bundle,
		});
	}
});
cur_frm.cscript['Product Bundle'] = function() {
	frappe.model.open_mapped_doc({
		method: "preorder.preorder.doctype.product_assembly.product_assembly.make_product_bundle",
		frm: cur_frm
	})
}
