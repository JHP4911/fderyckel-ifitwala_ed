# -*- coding: utf-8 -*-
# Copyright (c) 2020, ifitwala and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils  import getdate
from frappe.desk.reportview import get_match_cond, get_filters_cond
from frappe.model.document import Document

class LearningUnit(Document):
	def validate(self):
		if self.start_date and self.end_date and getdate(self.start_date) > getdate(self.end_date):
			frappe.throw(_("The start of the unit {0} cannot be after its end {1}.  Please adjust the dates").format(self.start_date, self.end_date))


# from JS. to filter out course that are only present in the program list of courses.
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_courses(doctype, txt, searchfield, start, page_len, filters):
	if filters.get('program'):
		return frappe.db.sql("""select course, course_name from `tabProgram Course`
			where  parent = %(program)s and course like %(txt)s {match_cond}
			order by
				if(locate(%(_txt)s, course), locate(%(_txt)s, course), 99999),
				idx desc,
				`tabProgram Course`.course asc
			limit {start}, {page_len}""".format(
				match_cond=get_match_cond(doctype),
				start=start,
				page_len=page_len), {
					"txt": "%{0}%".format(txt),
					"_txt": txt.replace('%', ''),
					"program": filters['program']
				})
