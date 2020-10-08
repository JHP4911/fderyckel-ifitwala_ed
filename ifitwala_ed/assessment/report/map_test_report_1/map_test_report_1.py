# Copyright (c) 2013, ifitwala and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_columns(filters)
	data = get_data(filters)

	return columns, data

def validate_filters(filters):
	''' Validate if dates are properly set '''
	if filters.start_date > filters.end_date:
		frappe.throw(_("Start Date must be before End Date."))


def get_data(filters = None):
	data = []
	conditions = get_filter_conditions(filters)
	map_results = frappe.db.sql("""
			SELECT student, student_name, program, test_percentile, test_rit_score, test_date, discipline
			FROM `tabMAP Test`
			WHERE
					docstatus = 0 %s
			ORDER BY
					test_date, discipline, test_rit_score""" % (conditions),  as_dict=1)

	for test in map_results:
		data.append({
				'student': test.student,
				'discipline': test.discipline,
				'student_name': test.student_name,
				'program': test.program,
				'test_rit_score': test.test_rit_score,
				'test_percentile': test.test_percentile,
				'test_date': test.test_date
		})

	return data


def get_columns(filters=None):
	columns = [
		{
			"label": _("Test Date"),
			"fieldname": "test_date",
			"fieldtype": "Date",
			"width": 100
		},
		{
			"label": _("Program"),
			"fieldname": "program",
			"fieldtype": "Link",
			"options": "Program",
			"width": 100
		},
		{
			"label": _("Student"),
			"fieldname": "student",
			"fieldtype": "Link",
			"options": "Student",
			"width": 150
		},
		{
			"label": _("Student Name"),
			"fieldname": "student_name",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Discipline"),
			"fieldname": "discipline",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("RIT Score"),
			"fieldname": "test_rit_score",
			"fieldtype": "Data",
			"width": 80
		},
		{
			"label": _("Percentile"),
			"fieldname": "test_percentile",
			"fieldtype": "Data",
			"width": 80
		}

	]
	return columns


def get_filter_conditions(filters):
	conditions = ""

	if filters.get("start_date"):
		conditions += " and test_date >= '%s' " % (filters.get("start_date"))

	if filters.get("end_date"):
		conditions += " and test_date <= '%s' " % (filters.get("end_date"))

	if filters.get("discpline"):
		conditions += " and program = '%s' " % (filters.get("discpline"))

	return conditions
