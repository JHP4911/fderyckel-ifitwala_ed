// Copyright (c) 2020, ifitwala and contributors
// For license information, please see license.txt

cur_frm.add_fetch('student', 'student_gender', 'gender');
cur_frm.add_fetch('student', 'student_date_of_birth', 'date_of_birth');
cur_frm.add_fetch('student', 'student_preferred_name', 'preferred_name');
cur_frm.add_fetch('student', 'student_full_name', 'student_name');

frappe.ui.form.on('Student Patient', {
	refresh: function(frm) {

	}
});
