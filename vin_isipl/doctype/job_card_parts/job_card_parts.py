# Copyright (c) 2026, harsh@buildwithhussain.com and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class JobCardParts(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		issued_by: DF.Link
		issued_date: DF.Date
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		part_name: DF.Data
		part_number: DF.Data
		quantity: DF.Int
		received_by: DF.Link
		signature: DF.AttachImage | None
	# end: auto-generated types
	pass
