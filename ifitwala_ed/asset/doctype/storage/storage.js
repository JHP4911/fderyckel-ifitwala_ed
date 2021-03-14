// Copyright (c) 2021, ifitwala and contributors
// For license information, please see license.txt

frappe.ui.form.on('Storage', {
	refresh: function(frm) {
    frm.toggle_display('storage_name', frm.doc.__islocal);

    if (cint(frm.doc.is_group) == 1) {
			frm.add_custom_button(__('Group to Non-Group'),
				function() { convert_to_group_or_ledger(frm); }, 'fa fa-retweet', 'btn-default')
		} else if (cint(frm.doc.is_group) == 0) {
			frm.add_custom_button(__('Non-Group to Group'),
				function() { convert_to_group_or_ledger(frm); }, 'fa fa-retweet', 'btn-default')
		}

    frm.toggle_enable(['is_group', 'school'], false);

		frappe.dynamic_link = {doc: frm.doc, fieldname: 'name', doctype: 'Storage'};

		frm.fields_dict['parent_storage'].get_query = function(doc) {
			return {
				filters: {
					"is_group": 1,
				}
			}
		}

		frm.fields_dict['account'].get_query = function(doc) {
			return {
				filters: {
					"is_group": 0,
					"account_type": "Stock",
					"school": frm.doc.school
				}
			}
		}
	}
});

function convert_to_group_or_ledger(frm){
	frappe.call({
		method:"ifitwala_ed.asset.doctype.storage.storage.convert_to_group_or_ledger",
		args: {
			docname: frm.doc.name,
			is_group: frm.doc.is_group
		},
		callback: function(){
			frm.refresh();
		}

	})
}
