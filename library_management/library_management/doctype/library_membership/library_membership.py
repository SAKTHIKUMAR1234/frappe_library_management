# Copyright (c) 2024, SAKTHI KUMAR P and contributors
# For license information, please see license.txt

import frappe
from frappe.model.docstatus import DocStatus
from frappe.model.document import Document


class LibraryMembership(Document):
	
	def before_validate(self) : 
		self.full_name = frappe.get_doc("Library Member",self.library_member).full_name

	def before_submit(self):
		exists = frappe.db.exists(
           "Library Membership",
           {
               "library_member": self.library_member,
               "docstatus": DocStatus.submitted(),
               "to_date": (">", self.from_date),
           },)
		if exists:
			frappe.throw("There is an active membership for this member")