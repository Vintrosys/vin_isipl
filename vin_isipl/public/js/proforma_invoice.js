frappe.ui.form.on('Quotation', {
    
    refresh: function (frm) {
        setTimeout(() => {
            $(frm.page.wrapper).find('.btn:contains("Get Items From")').remove();
        }, 5);


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
    },

    order_type: function (frm) {
        if (frm.doc.order_type == "STKPI" || frm.doc.order_type == "IMPPI") {
            frm.set_value('company', 'INNOVATIVE SEWING INDIA PRIVATE LIMITED');
        } else if (frm.doc.order_type == "SPPI" || frm.doc.order_type == "SRPI") {
            frm.set_value('company', 'INNOVATIVE');
        }
        if (frm.doc.order_type == "IMPPI") {
            frm.set_value('currency', 'USD');
            frm.set_df_property('tc_name', 'reqd', 0); 
            frm.set_df_property('tc_name', 'hidden', 1); 

        } else {
            frm.set_value('currency', 'INR');
            frm.set_df_property('tc_name', 'reqd', 1); 
            frm.set_df_property('tc_name', 'hidden', 0); 
        }
    },

    company: function (frm) {
        if (frm.doc.company == "INNOVATIVE SEWING INDIA PRIVATE LIMITED") {
            frm.set_value('naming_series', 'ISIPL-TPR-.FY.####');
        } else if (frm.doc.company == "INNOVATIVE") {
            frm.set_value('naming_series', 'INN-TPR-.FY.####');
        }
    },  

    party_name: function (frm) {
        if (frm.doc.party_name) {
            frappe.db.get_value('CRM Deal', { organization: frm.doc.party_name }, 'deal_owner')
                .then(r => {
                    if (r.message && r.message.deal_owner) {
                        fetch_sales_person(frm, r.message.deal_owner);
                    } else {
                        frm.set_value('sales_person', '');
                    }
                });
        } else {
            frm.set_value('sales_person', '');
        }
    }
});

function fetch_sales_person(frm, deal_owner) {    
    ee
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

