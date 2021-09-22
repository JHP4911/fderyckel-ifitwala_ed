# Copyright (c) 2021, ifitwala and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import time_diff_in_seconds
from ifitwala_ed.hr.doctype.employee.employee import get_employee_emails

class TrainingEvent(Document):
	def validate(self):
		self.set_employee_emails()
		self.validate_period()

	def on_update_after_submit(self):
		self.set_status_for_attendees()

	def set_employee_emails(self):
		self.employee_emails = ', '.join(get_employee_emails([d.employee for d in self.employees]))

	def validate_period(self):
		if time_diff_in_seconds(self.end_time, self.start_time) <= 0:
			frappe.throw(_("Your training event start time has to be earlier than the end time."))

	def set_status_for_attentdees(self):
		if self.event_status == "Completed":
			for employee in self.employees:
				if employee.attendance == "Present" and employee.status != "Feedback Submitted":
					employee.status = "Completed"

		elif self.event_status == "Scheduled":
			for employee in self.employees:
				employee.status = "Open"

		self.db_update_all()
