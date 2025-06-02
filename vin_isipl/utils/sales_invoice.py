import frappe
from vin_isipl.utils.pdf import attach_pdf
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice as OriginalSalesInvoice, get_discounting_status, get_total_in_party_account_currency, is_overdue
from frappe.utils import flt, getdate, nowdate


class CustomSalesInvoice(OriginalSalesInvoice):
    def set_status(self, update=False, status=None, update_modified=True):
        if self.is_new():
            if self.get("amended_from"):
                self.status = "Draft"
            return

        outstanding_amount = flt(self.outstanding_amount, self.precision("outstanding_amount"))
        total = get_total_in_party_account_currency(self)

        if not status:
            if self.docstatus == 2:
                status = "Cancelled"
            elif self.docstatus == 1:
                if self.is_internal_transfer():
                    self.status = "Internal Transfer"
                elif 0 < outstanding_amount < total:
                    self.status = "Partly Paid"
                elif is_overdue(self, total):
                    self.status = "Overdue"                
                elif outstanding_amount > 0 and getdate(self.due_date) >= getdate():
                    self.status = "Unpaid"
                # Check if outstanding amount is 0 due to credit note issued against invoice
                elif self.is_return == 0 and frappe.db.get_value(
                    "Sales Invoice", {"is_return": 1, "return_against": self.name, "docstatus": 1}
                ):
                    self.status = "Credit Note Issued"
                elif self.is_return == 1:
                    self.status = "Return"
                elif outstanding_amount <= 0:
                    self.status = "Paid"
                else:
                    self.status = "Submitted"

                if (
                    self.status in ("Unpaid", "Partly Paid", "Overdue")
                    and self.is_discounted
                    and get_discounting_status(self.name) == "Disbursed"
                ):
                    self.status += " and Discounted"

            else:
                self.status = "Draft"

        if update:
            self.db_set("status", self.status, update_modified=update_modified)

def on_update(doc, method=None):
    
    print_format_map = {
        "*": "Commercial Invoice"
    }
    
    frappe.enqueue(
        method="vin_isipl.utils.pdf.attach_pdf",
        queue='long',
        timeout=300,
        job_name=f"Attach PDF for {doc.doctype} {doc.name}",
        doc=doc,
        print_format_map=print_format_map
    )
