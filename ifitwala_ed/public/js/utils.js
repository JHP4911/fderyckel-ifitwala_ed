// Copyright (c) 2020, ifitwala and contributors
// For license information, please see license.txt

frappe.provide("ifitwala_ed");
frappe.provide("ifitwala_ed.utils");

$.extend(ifitwala_ed, {
	get_currency: function(organization) {
		if(!organization && cur_frm)
			organization = cur_frm.doc.organization;
		if(organization)
			return frappe.get_doc(":Organization", organization).default_currency || frappe.boot.sysdefaults.currency;
		else
			return frappe.boot.sysdefaults.currency;
	},

	get_presentation_currency_list: () => {
		const docs = frappe.boot.docs;
		let currency_list = docs.filter(d => d.doctype === ":Currency").map(d => d.name);
		currency_list.unshift("");
		return currency_list;
	},
	is_perpetual_inventory_enabled: function(organization) {
		if(organization) {
			return frappe.get_doc(":Organization", organization).enable_perpetual_inventory
		}
	},

	toggle_naming_series: function() {
		if(cur_frm.fields_dict.naming_series) {
			cur_frm.toggle_display("naming_series", cur_frm.doc.__islocal?true:false);
		}
	},

	hide_organization: function() {
		if(cur_frm.fields_dict.organization) {
			var companies = Object.keys(locals[":Organization"] || {});
			if(companies.length === 1) {
				if(!cur_frm.doc.organization) cur_frm.set_value("organization", companies[0]);
				cur_frm.toggle_display("organization", false);
			} else if(erpnext.last_selected_organization) {
				if(!cur_frm.doc.organization) cur_frm.set_value("organization", erpnext.last_selected_organization);
			}
		}
	}
});

$.extend(ifitwala_ed.utils, {
	copy_value_in_all_rows: function(doc, dt, dn, table_fieldname, fieldname) {
		var d = locals[dt][dn];
		if(d[fieldname]){
			var cl = doc[table_fieldname] || [];
			for(var i = 0; i < cl.length; i++) {
				if(!cl[i][fieldname]) cl[i][fieldname] = d[fieldname];
			}
		}
		refresh_field(table_fieldname);
	},

	get_tree_options: function(option) {
		// get valid options for tree based on user permission & locals dict
		let unscrub_option = frappe.model.unscrub(option);
		let user_permission = frappe.defaults.get_user_permissions();
		let options;

		if(user_permission && user_permission[unscrub_option]) {
			options = user_permission[unscrub_option].map(perm => perm.doc);
		} else {
			options = $.map(locals[`:${unscrub_option}`], function(c) { return c.name; }).sort();
		}
		// filter unique values, as there may be multiple user permissions for any value
		return options.filter((value, index, self) => self.indexOf(value) === index);
	},

	get_tree_default: function(option) {
		// set default for a field based on user permission
		let options = this.get_tree_options(option);
		if(options.includes(frappe.defaults.get_default(option))) {
			return frappe.defaults.get_default(option);
		} else {
			return options[0];
		}
	}

});

frappe.form.link_formatters['Employee'] = function(value, doc) {
	if(doc && doc.employee_full_name && doc.employee_full_name !== value) {
		return value? value + ': ' + doc.employee_full_name: doc.employee_full_name;
	} else {
		return value;
	}
}
