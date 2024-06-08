# Copyright (c) 2024, SAKTHI KUMAR P and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.document import DocStatus


class LibraryTransaction(Document):
    def before_save(self):
        if self.type == "issue":
            self.validate_issue()
            article = frappe.get_doc("Article", self.article)
            article.status = "Issued"
            article.save()

        elif self.type == "return":
            self.validate_return()
            article = frappe.get_doc("Article", self.article)
            article.status = "Available"
            article.save()

    def validate_issue(self):
        self.validate_membership()
        article = frappe.get_doc("Article", self.article)
        if article.status == "Issued":
            frappe.throw("Article is already issued by another member")

    def validate_return(self):
        article = frappe.get_doc("Article", self.article)
        if article.status == "Available":
            frappe.throw("Article cannot be returned without being issued first")

    def validate_membership(self):
        valid_membership = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": DocStatus.submitted(),
                "from_date": ("<", self.transaction_date),
                "to_date": (">", self.transaction_date),
            },
        )
        if not valid_membership:
            frappe.throw("The member does not have a valid membership")


