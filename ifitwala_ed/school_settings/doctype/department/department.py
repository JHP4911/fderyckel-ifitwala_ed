# -*- coding: utf-8 -*-
# Copyright (c) 2020, ifitwala and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils.user import add_role
from frappe.model.document import Document
from frappe.email.doctype.email_group.email_group import add_subscribers


class Department(Document):

	def autoname(self):
		if self.organization and not self.school:
			self.name = self.department_name + " - {}".format(self.organization_abbreviation) if self.organization_abbreviation else ""
		if self.school:
			self.name = self.department_name + " - {}".format(self.school_abbreviation) if self.school_abbreviation else ""
		if not self.organization and not self.school:
			self.name = self.department_name

	def validate(self):
		# You cannot have 2 dpt. of the same within the same organization. OK in 2 different organization.
		self.validate_duplicate()
		if self.organization and not self.school:
			self.title = self.department_name + " - {}".format(self.organization_abbreviation) if self.organization_abbreviation else ""
		if self.school:
			self.title = self.department_name + " - {}".format(self.school_abbreviation) if self.school_abbreviation else ""
		if not self.organization and not self.school:
			self.title = self.department_name

		found = []
		for member in self.members:
			if member.member in found:
				frappe.throw(_("You have already added the member {0} to the Department. Please remove it.").format(member.member))
			found.append(member.member)
		if self.department_lead and (self.department_lead not in found):
			self.append("members", {"member": self.department_lead})
			frappe.msgprint(_("{0} added as a member of the department.").format(self.department_lead))
		if self.department_lead:
			roles = frappe.get_roles(self.department_lead)
			if "Newsletter Manager" not in roles:
				add_role(self.department_lead, "Newsletter Manager")
				frappe.msgprint(_("Added the Newsletter role to {0} as Department Lead.").format(self.department_lead))

	def validate_duplicate(self):
    		dpt = frappe.db.sql("""select name from `tabDepartment` where organization= %s and department_name= %s and docstatus<2 and name != %s""", (self.organization, self.department_name, self.name))
    		if dpt:
       			frappe.throw(_("A department within this organization {0} and this name {1} already exisit. Please adjust the name as necessary.").format(self.organization, self.department_name))


@frappe.whitelist()
def get_department_members(department):
    """ Return the list of all members from a dpt"""
    members = frappe.get_list("Department Member", fields = ["member", "member_name"],
                filters = {"parent": department}, order_by = "member")
    return members

@frappe.whitelist()
def update_dpt_email(doctype, name):
    if not frappe.db.exists("Email Group"):
        d_mail_group = frappe.new_doc("Email Group")
        d_mail_group.title = name
        d_mail_group.save()
    members_mail_list = []
    members = []
    if doctype == "Department":
        members = get_department_members(name)
    for member in members:
        m_mail = frappe.get_value("Employee", {"user_id": member.member}, "employee_professional_email")
        if m_mail:
            members_mail_list.append(m_mail)
    add_subscribers(name, members_mail_list)

@frappe.whitelist()
def create_prefilled_newsletter():
	newsletter = frappe.new_doc("Newsletter")
	newsletter.subject = ("{0} Newsletter").format(self.department_name)
	newsletter.append("email_group", {"email_group":self.department_name})
	newsletter.save()
	return newsletter.name
