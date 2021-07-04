from __future__ import unicode_literals
import frappe, os, json
from frappe import _
from frappe.desk.page.setup_wizard.setup_wizard import make_records
from frappe.utils import cstr, getdate
from frappe.desk.doctype.global_search_settings.global_search_settings import update_global_search_doctypes

from ifitwala_ed.accounting.doctype.account.account import RootNotEditable

def install(country=None):
	records = [
		# item group
		{'doctype': 'Item Group', 'item_group_name': _('All Item Groups'), 'is_group': 1, 'parent_item_group': ''},

		# Employment Type
		{'doctype': 'Employment Type', 'employment_type_name': _('Full-time')},
		{'doctype': 'Employment Type', 'employment_type_name': _('Part-time')},
		{'doctype': 'Employment Type', 'employment_type_name': _('Probation')},
		{'doctype': 'Employment Type', 'employment_type_name': _('Contract')},
		{'doctype': 'Employment Type', 'employment_type_name': _('Intern')},
		{'doctype': 'Employment Type', 'employment_type_name': _('Apprentice')},

		# Mode of Payment
		{'doctype': 'Mode of Payment', 'mode_of_payment': 'Check' if country=="United States" else _('Cheque'), 'type': 'Bank'},
		{'doctype': 'Mode of Payment', 'mode_of_payment': _('Cash'), 'type': 'Cash'},
		{'doctype': 'Mode of Payment', 'mode_of_payment': _('Credit Card'), 'type': 'Bank'},
		{'doctype': 'Mode of Payment', 'mode_of_payment': _('Wire Transfer'), 'type': 'Bank'},
		{'doctype': 'Mode of Payment', 'mode_of_payment': _('Bank Draft'), 'type': 'Bank'},

		{'doctype': "Party Type", "party_type": "Supplier", "account_type": "Payable"},
		{'doctype': "Party Type", "party_type": "Employee", "account_type": "Payable"},
		{'doctype': "Party Type", "party_type": "Student", "account_type": "Receivable"},

		{"doctype": "Designation", "designation_name": "Director"},
		{"doctype": "Designation", "designation_name": "Principal"},
		{"doctype": "Designation", "designation_name": "Assistant Principal"},
		{"doctype": "Designation", "designation_name": "Nurse"},
		{"doctype": "Designation", "designation_name": "Teacher"},
		{"doctype": "Designation", "designation_name": "Teacher Assistant"},

		{"doctype": "Student Log Type", "log_type": "Behaviour"},
		{"doctype": "Student Log Type", "log_type": "Academic"},
		{"doctype": "Student Log Type", "log_type": "Medical"},

		{"doctype": "Student Attendance Code", "attendance_code": "Present"},
		{"doctype": "Student Attendance Code", "attendance_code": "Absent"},
		{"doctype": "Student Attendance Code", "attendance_code": "Tardy"},
		{"doctype": "Student Attendance Code", "attendance_code": "Excused Absence"},
		{"doctype": "Student Attendance Code", "attendance_code": "Field Trip"},
		{"doctype": "Student Attendance Code", "attendance_code": "Excused Tardy"},

		{"doctype": "Location Type", "location_type_name": "Classroom"},
		{"doctype": "Location Type", "location_type_name": "Office"},
		{"doctype": "Location Type", "location_type_name": "School"},
		{"doctype": "Location Type", "location_type_name": "Building"},
		{"doctype": "Location Type", "location_type_name": "Storage"}
	]
	make_records(records)
	set_more_defaults()
	update_global_search_doctypes()

def set_more_defaults():
	add_uom_data()


def add_uom_data():
	# add UOMs
	uoms = json.loads(open(frappe.get_app_path("ifitwala_ed", "setup", "setup_wizard", "data", "uom_data.json")).read())
	for d in uoms:
		if not frappe.db.exists('UOM', _(d.get("uom_name"))):
			uom_doc = frappe.get_doc({
				"doctype": "UOM",
				"uom_name": _(d.get("uom_name")),
				"name": _(d.get("uom_name")),
				"must_be_whole_number": d.get("must_be_whole_number")
			}).insert(ignore_permissions=True)

		# bootstrap uom conversion factors
	uom_conversions = json.loads(open(frappe.get_app_path("ifitwala_ed", "setup", "setup_wizard", "data", "uom_conversion_data.json")).read())
	for d in uom_conversions:
		if not frappe.db.exists("UOM Category", _(d.get("category"))):
			frappe.get_doc({
				"doctype": "UOM Category",
				"category_name": _(d.get("category"))
			}).insert(ignore_permissions=True)

		if not frappe.db.exists("UOM Conversion Factor", {"from_uom": _(d.get("from_uom")), "to_uom": _(d.get("to_uom"))}):
			uom_conversion = frappe.get_doc({
				"doctype": "UOM Conversion Factor",
				"category": _(d.get("category")),
				"from_uom": _(d.get("from_uom")),
				"to_uom": _(d.get("to_uom")),
				"value": d.get("value")
			}).insert(ignore_permissions=True)


def install_organization(args):
	records = [
		# Fiscal Year
		{
			'doctype': "Fiscal Year",
			'year': get_fy_details(args.fy_start_date, args.fy_end_date),
			'year_start_date': args.fy_start_date,
			'year_end_date': args.fy_end_date
		},

		# Organization
		{
			"doctype":"Organization",
			'organization_name': args.organization_name,
			'enable_perpetual_inventory': 1,
			'abbr': args.organization_abbr,
			'default_currency': args.currency,
			'country': args.country,
			'create_chart_of_accounts_based_on': 'Standard Template',
			'chart_of_accounts': args.chart_of_accounts,
		}
	]

	make_records(records)


#def install_post_organization_fixtures(args=None):
#	records = [
#		# Department
#		{'doctype': 'Team', 'team_name': _('All Departments'), 'is_group': 1, 'parent_team': ''},
#		{'doctype': 'Team', 'team_name': _('Accounts'), 'parent_team': _('All Departments'), 'organization': args.organization_name},
#		{'doctype': 'Team', 'team_name': _('Operations'), 'parent_team': _('All Departments'), 'organization': args.organization_name},
#		{'doctype': 'Team', 'team_name': _('Human Resources'), 'parent_team': _('All Departments'), 'organization': args.organization_name},
#		{'doctype': 'Team', 'team_name': _('Legal'), 'parent_team': _('All Departments'), 'organization': args.organization_name},
#	]
#	make_records(records)

def install_defaults(args=None):
	# enable default currency
	frappe.db.set_value("Currency", args.get("currency"), "enabled", 1)
	global_defaults = frappe.get_doc("Global Defaults", "Global Defaults")
	current_fiscal_year = frappe.get_all("Fiscal Year")[0]
	global_defaults.update({
		'current_fiscal_year': current_fiscal_year.name,
		'default_currency': args.get('currency'),
		'default_organization':args.get('organization_name'),
		"country": args.get("country")
		})

	global_defaults.save()

	system_settings = frappe.get_doc("System Settings")
	system_settings.email_footer_address = args.get("organization_name")
	system_settings.save()

	if args.bank_account:
		organization_name = args.organization_name
		bank_account_group =  frappe.db.get_value("Account", {"account_type": "Bank", "is_group": 1, "root_type": "Asset", "organization": organization_name})
		if bank_account_group:
			bank_account = frappe.get_doc({
				"doctype": "Account",
				'account_name': args.bank_account,
				'parent_account': bank_account_group,
				'is_group':0,
				'organization': organization_name,
				"account_type": "Bank",
			})
			try:
				doc = bank_account.insert()

				frappe.db.set_value("Organization", args.organization_name, "default_bank_account", bank_account.name, update_modified=False)

			except RootNotEditable:
				frappe.throw(_("Bank account cannot be named as {0}").format(args.bank_account))
			except frappe.DuplicateEntryError:
				# bank account same as a CoA entry
				pass


def get_fy_details(fy_start_date, fy_end_date):
	start_year = getdate(fy_start_date).year
	if start_year == getdate(fy_end_date).year:
		fy = cstr(start_year)
	else:
		fy = cstr(start_year) + '-' + cstr(start_year + 1)
	return fy
