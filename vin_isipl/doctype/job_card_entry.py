# Copyright (c) 2026, harsh@buildwithhussain.com and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class JobCardEntry(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from forms_pro.forms_pro.doctype.job_card_parts.job_card_parts import JobCardParts
		from frappe.types import DF

		amended_from: DF.Link | None
		assurance_given_if_any: DF.LongText | None
		authorised_by: DF.Data
		company_name: DF.Link
		completed_by: DF.Link
		completed_date: DF.Date
		completed_time: DF.Time
		delivered_by: DF.Link
		delivery_date: DF.Date
		delivery_time: DF.Time
		details_of_work_done: DF.SmallText
		job_card_date: DF.Date
		job_card_number: DF.Data
		labour_charges: DF.Currency
		machine_model_no: DF.Data
		machine_problem_description: DF.LongText
		machine_received_by: DF.Link
		machine_received_date_and_time: DF.Datetime | None
		machine_serial_no: DF.Data
		parts_used: DF.Table[JobCardParts]
		problem_completed: DF.Literal["Full", "Partial"]
		status_of_machine_at_present: DF.SmallText
	# end: auto-generated types
	pass
