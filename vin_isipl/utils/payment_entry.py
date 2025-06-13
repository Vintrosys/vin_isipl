import frappe
from erpnext.accounts.doctype.payment_entry.payment_entry import PaymentEntry as ERPNextPaymentEntry
from frappe import _

class CustomPaymentEntry(ERPNextPaymentEntry):
    def validate_transaction_reference(self):
        bank_account = self.paid_to if self.payment_type == "Receive" else self.paid_from
        bank_account_type = frappe.get_cached_value("Account", bank_account, "account_type")

        if bank_account_type == "Bank":
            if self.mode_of_payment and self.mode_of_payment.lower() == "neft":
                return

            if not self.reference_no or not self.reference_date:
                frappe.throw(_("Reference No and Reference Date is mandatory for Bank transaction"))
