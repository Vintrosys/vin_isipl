import frappe
from hrms.mixins.pwa_notifications import PWANotificationsMixin, bold
from hrms.hr.doctype.leave_application.leave_application import LeaveApplication
from hrms.hr.doctype.expense_claim.expense_claim import ExpenseClaim

class CustomPWANotificationsMixin(PWANotificationsMixin):

	def notify_approval_status(self):
		status_field = self._get_doc_status_field()
		status = self.get(status_field)

		# Notify the applicant when Approved/Rejected
		if self.has_value_changed(status_field) and status in ["Approved", "Rejected"]:
			from_user = frappe.session.user
			from_user_name = self._get_user_name(from_user)
			to_user = self._get_employee_user()

			# Avoid notifying self
			if from_user == to_user:
				return

			# Notify applicant
			self._create_pwa_notification(
				from_user,
				to_user,
				f"{bold('Your')} {bold(self.doctype)} {self.name} has been {bold(status)} by {bold(from_user_name)}"
			)

			# Notify approver when rejected
			if status == "Rejected":
				to_user = self.leave_approver
				self._create_pwa_notification(
					from_user,
					to_user,
					f"{self.employee_name}'s {self.doctype} {self.name} has been {bold(status)} by {bold(from_user_name)}"
				)

		# Workflow-based notifications
		wf_state = self.workflow_state
		leave_authorizer = frappe.db.get_value(
			"Department Approver",
			{"parent": self.department, "parentfield": "leave_approvers", "idx": 2},
			"approver"
		)

		# Notify authorizer when Approved
		if wf_state == "Approved":
			from_user = self.leave_approver
			to_user = leave_authorizer
			self._create_pwa_notification(
				from_user,
				to_user,
				f"{self.employee_name} raised a new {self.doctype} to authorize: {self.name}"
			)

		# Notify applicant & approver when Authorized
		if wf_state == "Authorized":
			from_user = leave_authorizer
			from_user_name = self._get_user_name(from_user)
			to_user = self._get_employee_user()

			# Notify applicant
			self._create_pwa_notification(
				from_user,
				to_user,
				f"{bold('Your')} {bold(self.doctype)} {self.name} has been {bold(wf_state)} by {bold(from_user_name)}"
			)

			# Notify approver
			to_user = self.leave_approver
			self._create_pwa_notification(
				from_user,
				to_user,
				f"{self.employee_name}'s {self.doctype} {self.name} has been {bold(wf_state)} by {bold(from_user_name)}"
			)

	def _create_pwa_notification(self, from_user, to_user, message):
		"""Utility method to create PWA Notification docs cleanly"""
		notification = frappe.new_doc("PWA Notification")
		notification.from_user = from_user
		notification.to_user = to_user
		notification.message = message
		notification.reference_document_type = self.doctype
		notification.reference_document_name = self.name
		notification.insert(ignore_permissions=True)


class CustomLeaveApplication(LeaveApplication, CustomPWANotificationsMixin):
	pass

import frappe
from hrms.mixins.pwa_notifications import PWANotificationsMixin, bold
from hrms.hr.doctype.expense_claim.expense_claim import ExpenseClaim


class CustomExpensePWANotificationsMixin(PWANotificationsMixin):
    def notify_approval_status(self):
        status_field = self._get_doc_status_field()
        status = self.get(status_field)

        if self.has_value_changed(status_field) and status in ["Approved", "Rejected"]:
            from_user = frappe.session.user
            self._notify_applicant_and_approver(from_user, status)

        wf_state = self.workflow_state
        expense_authorizer = frappe.db.get_value(
            "Department Approver",
            {"parent": self.department, "parentfield": "expense_approvers", "idx": 2},
            "approver",
        )

        if wf_state == "Approved":
            from_user = self.expense_approver
            if expense_authorizer:
                self._create_pwa_notification(
                    from_user,
                    expense_authorizer,
                    f"{self.employee_name} raised a new {self.doctype} to authorize: {self.name}"
                )
            self._notify_applicant(from_user, "Approved")

        if wf_state == "Authorized":
            from_user = expense_authorizer
            self._notify_applicant_and_approver(from_user, "Authorized")

        if wf_state == "Rejected":
            from_user = expense_authorizer
            self._notify_applicant_and_approver(from_user, "Rejected")

    def _notify_applicant_and_approver(self, from_user, status):
        from_user_name = self._get_user_name(from_user)

        self._create_pwa_notification(
            from_user,
            self._get_employee_user(),
            f"{bold('Your')} {bold(self.doctype)} {self.name} has been {bold(status)} by {bold(from_user_name)}"
        )

        if self.expense_approver and self.expense_approver != from_user:
            self._create_pwa_notification(
                from_user,
                self.expense_approver,
                f"{self.employee_name}'s {self.doctype} {self.name} has been {bold(status)} by {bold(from_user_name)}"
            )

    def _notify_applicant(self, from_user, status):
        from_user_name = self._get_user_name(from_user)
        self._create_pwa_notification(
            from_user,
            self._get_employee_user(),
            f"{bold('Your')} {bold(self.doctype)} {self.name} has been {bold(status)} by {bold(from_user_name)}"
        )

    def _create_pwa_notification(self, from_user, to_user, message):
        if not to_user:
            return

        notification = frappe.new_doc("PWA Notification")
        notification.from_user = from_user
        notification.to_user = to_user
        notification.message = message
        notification.reference_document_type = self.doctype
        notification.reference_document_name = self.name
        notification.insert(ignore_permissions=True)


class CustomExpenseClaim(ExpenseClaim, CustomExpensePWANotificationsMixin):
    pass

