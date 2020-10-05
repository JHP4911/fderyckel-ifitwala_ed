# -*- coding: utf-8 -*-
# Copyright (c) 2020, ifitwala and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.desk.reportview import get_match_cond, get_filters_cond
from frappe.model.document import Document 
from frappe import _

class Meeting(Document):
	
	def validate(self): 
		self.validate_attendees() 
		if not self.attendees: 
			self.extend("attendees", self.get_attendees()) 
		
	def validate_attendees(self): 
		found = []
		for attendee in self.attendees: 
			if attendee.attendee in found: 
				frappe.throw(_("Attendee {0} entered twice.").format(attendee.attendee))
			found.append(attendee.attendee)
			
	def get_attendees(self): 
		return frappe.db.sql("""select member from `tabDepartment Member` where parent = %s""", (self.department), as_dict=1)
			
			
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_department_members(doctype, txt, searchfield, start, page_len, filters):
	if filters.get('department'):
		return frappe.db.sql("""select member, member_name from `tabDepartment Member`
			where  parent = %(department)s and members like %(txt)s {match_cond}
			order by
				if(locate(%(_txt)s, member), locate(%(_txt)s, member), 99999),
				idx desc,
				`tabDepartment Member`.member asc
			limit {start}, {page_len}""".format(
				match_cond=get_match_cond(doctype),
				start=start,
				page_len=page_len), {
					"txt": "%{0}%".format(txt),
					"_txt": txt.replace('%', ''),
					"department": filters['department']
				})
