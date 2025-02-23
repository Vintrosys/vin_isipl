import click
import frappe

from vin_isipl.install import get_custom_fields

def before_uninstall():
	print("Removing customizations created by the Vin ISIPL app...")
	remove_custom_fields()

	click.secho("Vin ISIPL customizations have been removed successfully...", fg="green")

def remove_custom_fields():
	for doctype, fields in get_custom_fields().items():
		frappe.db.delete(
			"Custom Field",
			{
				"fieldname": ("in", [field["fieldname"] for field in fields]),
				"dt": doctype,
			},
		)

		frappe.clear_cache(doctype=doctype)
