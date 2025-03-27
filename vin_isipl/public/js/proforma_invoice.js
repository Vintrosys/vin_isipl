frappe.ui.form.on('Quotation', {
    refresh: function (frm) {
        if (!frm.is_new()) {           
            frm.add_custom_button('Save to Table', function () {
                frappe.call({
                    method: "vin_isipl.utils.pi_version_tracker.save_to_table",
                    args: {
                        quotation_name: frm.doc.name
                    },
                    callback: function () {
                        frappe.show_alert({ message: __("Version Tracker Updated!"), indicator: 'green' });

                    }
                });
            });
        }
    }
});
