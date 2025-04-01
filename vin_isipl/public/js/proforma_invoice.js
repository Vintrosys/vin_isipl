frappe.ui.form.on('Quotation', {
    refresh: function (frm) {
        if (!frm.is_new()) {           
            frm.add_custom_button('Save PDF', function () {
                frappe.call({
                    method: "vin_isipl.utils.pi_version_tracker.save_to_table",
                    args: {
                        quotation_name: frm.doc.name
                    },
                    freeze: true,
                    callback: function () {
                        frappe.show_alert({ message: __("Version Tracker Updated!"), indicator: 'green' });

                    }
                });
            });
        }
    }
});

function fetch_sales_person(frm, deal_owner) {    
    frappe.db.get_value('Employee', { user_id: deal_owner }, 'name')
        .then(emp => {
            if (emp.message && emp.message.name) {               
                frappe.db.get_value('Sales Person', { employee: emp.message.name }, 'name')
                    .then(sp => {
                        frm.set_value('sales_person', sp.message.name);
                    });
            } else {
                frm.set_value('sales_person', '');
            }
            frm.refresh_field('sales_person');
        });
}

