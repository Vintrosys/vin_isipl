import frappe
from hrms.mixins.pwa_notifications import PWANotificationsMixin, bold
from hrms.hr.doctype.leave_application.leave_application import LeaveApplication


class CustomPWANotificationsMixin(PWANotificationsMixin):

	def notify_approval_status(self):

		status_field = self._get_doc_status_field()
		status = self.get(status_field)

		if self.has_value_changed(status_field) and status in ["Approved", "Rejected"]:
			from_user = frappe.session.user
			from_user_name = self._get_user_name(from_user)
			to_user = self._get_employee_user()

			if from_user == to_user:
				return

			notification = frappe.new_doc("PWA Notification")
			notification.from_user = from_user
			notification.to_user = to_user

			notification.message = f"{bold('Your')} {bold(self.doctype)} {self.name} has been {bold(status)} by {bold(from_user_name)}"

			notification.reference_document_type = self.doctype
			notification.reference_document_name = self.name
			notification.insert(ignore_permissions=True)

		wf_state = self.workflow_state

		if wf_state == "Approved":
			from_user = self.leave_approver
			to_user = self.custom_leave_authorizer
			notification = frappe.new_doc("PWA Notification")
			notification.message = (
				f"{self.employee_name} raised a new {self.doctype} to authorize: {self.name}"
			)
			notification.from_user = from_user
			notification.to_user = to_user
			notification.reference_document_type = self.doctype
			notification.reference_document_name = self.name
			notification.insert(ignore_permissions=True)

		if wf_state in ["Authorized"]:
			from_user = self.custom_leave_authorizer
			from_user_name = self._get_user_name(from_user)
			to_user = self._get_employee_user()
			notification = frappe.new_doc("PWA Notification")
			notification.message = f"{bold('Your')} {bold(self.doctype)} {self.name} has been {bold(wf_state)} by {bold(from_user_name)}"
			notification.from_user = from_user
			notification.to_user = to_user
			notification.reference_document_type = self.doctype
			notification.reference_document_name = self.name
			notification.insert(ignore_permissions=True)

class CustomLeaveApplication(LeaveApplication, CustomPWANotificationsMixin):
	pass
