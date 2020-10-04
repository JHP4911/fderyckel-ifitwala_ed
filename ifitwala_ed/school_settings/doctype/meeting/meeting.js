// Copyright (c) 2020, ifitwala and contributors
// For license information, please see license.txt

frappe.ui.form.on('Meeting', {
	
	onload: function(frm, cdt, cdn) { 
		if (frm.doc.department) {
			frm.set_query("attendee", "attendees", function(doc, cdt, cdn) {
				return{
					query: "ifitwala_ed.school_settings.doctype.meeting.meeting.get_department_members",
					filters: {
						'department': frm.doc.department
					}
				}
			});
		}

	}, 
	
	department: function(frm) {
		frm.events.get_attendees(frm);
	},
	
	get_attendees: function(frm) {
		frm.set_value('attendee',[]);
		frappe.call({
			method: 'get_attendees',
			doc:frm.doc,
			callback: function(r) {
				if(r.message) {
					frm.set_value('attendees', r.message);
				}
			}
		})
	}
});
