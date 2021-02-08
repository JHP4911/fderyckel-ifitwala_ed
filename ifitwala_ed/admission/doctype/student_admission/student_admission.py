# -*- coding: utf-8 -*-
# Copyright (c) 2020, ifitwala and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import nowdate
from frappe.website.website_generator import WebsiteGenerator

class StudentAdmission(WebsiteGenerator):
	def validate(self):
		self.title = self.page_name + " ({})".format(self.academic_year)
		if not self.route:
			self.route = "admission/" + "-".join(self.title.split(" "))
		if self.enable_admission_application and not self.program_details:
			frappe.throw(_("If Enable Admission Application is ticked you should add some programs."))

	def get_context(self, context):
		context.no_cache = 1
		context.show_sidebar = True
		context.title = self.title
		context.parents = [{
					"name": "admissions",
					"title": _("All Students Admission"),
					"route": "admissions"
				}]

def get_list_context(context=None):
	context.update({
		"show_sidebar": True, 
		"title": _("All Students Admission"),
		"get_list": get_admission_list,
		"row_template": "admission/doctype/student_admission/templates/student_admission_row.html",
	})

def get_admission_list(doctype, txt, filters, limit_start, limit_page_length=20, order_by="modified"):
	return frappe.db.sql('''select name, title, academic_year, modified, admission_start_date, route,
		admission_end_date from `tabStudent Admission` where published=1 and admission_end_date >= %s
		order by admission_end_date asc limit {0}, {1}
		'''.format(limit_start, limit_page_length), [nowdate()], as_dict=1)
