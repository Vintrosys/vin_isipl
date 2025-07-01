frappe.ui.form.on('Quotation', {
    
    refresh: function (frm) {

        setTimeout(() => {
            $(frm.page.wrapper).find('.btn:contains("Get Items From")').remove();
            // $(frm.page.wrapper).find('.btn:contains("Submit")').remove();
        }, 5);

        if (frm.doc.docstatus === 0 && frm.doc.order_type === "Import PI" && !frm._tax_reset_done) {
            update_tax_fields(frm);         
            frm._tax_reset_done = true;
        }        

        if (frm.doc.name && frm.doc.creation && frm.doc.docstatus < 2) {  
            frm.add_custom_button(__('Print PDF'), function () {
                let format = '';

                switch (frm.doc.order_type) {
                    case 'Stock PI':
                        format = 'Machine PI';
                        break;
                    case 'Import PI':
                        format = 'Import PI';
                        break;
                    case 'Spares PI':
                        format = 'Spares PI';
                        break;
                    case 'Service PI':
                        format = 'Service PI';
                        break;
                }

                let url = `/api/method/frappe.utils.print_format.download_pdf?doctype=${frm.doc.doctype}&name=${frm.doc.name}&format=${format}`;
                window.open(url, '_blank');
            });
      
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
    
    party_name: function (frm) {
        frm.set_value('sales_person', '');
        frm.trigger('set_party_name');  
    },

    order_type: function (frm) {   
       
        if (frm.doc.order_type == "Stock PI" || frm.doc.order_type == "Import PI") {
            frm.set_value('company', 'ISIPL');
        } else if (frm.doc.order_type == "Spares PI" || frm.doc.order_type == "Service PI") {
            frm.set_value('company', 'INNOVATIVE');
        }

        setTimeout(() => {
            if (frm.doc.order_type == "Import PI") {
                frm.set_value('currency', 'USD');
                frm.set_df_property('tc_name', 'reqd', 0); 
                frm.set_df_property('tc_name', 'hidden', 1); 
            } else {
                frm.set_value('currency', 'INR');
                frm.set_df_property('tc_name', 'reqd', 1); 
                frm.set_df_property('tc_name', 'hidden', 0); 
            }

            frm.trigger('set_terms');
            update_tax_fields(frm);
        }, 300); 
    },

    company: function (frm) {
        if (frm.doc.company == "ISIPL") {
            frm.set_value('naming_series', 'ISIPL-TPR-.FY.####');
            frm.set_value('tc_name', '')
            frm.set_value('custom_isipl_bank_account', '');
            frm.set_value('payment_terms_template', '');
            frm.set_value('custom_shipping_term', '');
        } else if (frm.doc.company == "INNOVATIVE") {
            frm.set_value('naming_series', 'INN-TPR-.FY.####');
            frm.set_value('custom_isipl_bank_account', 'Innovative - IndusInd Bank');
            frm.set_value('payment_terms_template', 'Immediate');
            frm.set_value('custom_shipping_term', 'Ex - Works Tirupur');
            if (frm.doc.order_type == "Service PI") {
                frm.set_value('tc_name', 'Terms and Conditions - SERVICE AMC')
            } else {
                frm.set_value('tc_name', 'Terms and Conditions - STANDARD')
            }
        }
    },  
    
    set_terms: function (frm) {
        if (frm.doc.company == "ISIPL") {
            frm.set_value('tc_name', '')
        }
        else {
            if (frm.doc.order_type == "Service PI") {
                frm.set_value('tc_name', 'Terms and Conditions - SERVICE AMC')
            } else {
                frm.set_value('tc_name', 'Terms and Conditions - STANDARD')
            }
        }  

    },

    set_party_name: function (frm) {
        if (frm.doc.party_name) {
            frappe.db.get_value('CRM Deal', { organization: frm.doc.party_name }, 'deal_owner')
                .then(r => {
                    if (r.message && r.message.deal_owner) {
                        fetch_sales_person(frm, r.message.deal_owner);
                    } else {
                        if (!frm.doc.sales_person) {
                            frm.set_value('sales_person', '');
                        }
                    }
                });
                frappe.db.get_value('Customer', frm.doc.party_name, 'custom_sales_person')
                .then(r => {
                    if (r.message && r.message.custom_sales_person) {
                        frm.set_value('sales_person', r.message.custom_sales_person);
                    } else {
                        if (!frm.doc.sales_person) {
                            frm.set_value('sales_person', '');
                        }
                    }
                });
        } else {
            if (!frm.doc.sales_person) {
                frm.set_value('sales_person', '');
            }

        }
    }
});

function fetch_sales_person(frm, deal_owner) {    
    frappe.db.get_value('Employee', { user_id: deal_owner }, 'name')
        .then(emp => {
            if (emp.message && emp.message.name) {               
                frappe.db.get_value('Sales Person', { employee: emp.message.name }, 'name')
                    .then(sp => {
                        if (!frm.doc.sales_person) {
                            frm.set_value('sales_person', sp.message.name);
                        }
                    });
            } else {
                if (!frm.doc.sales_person) {
                    frm.set_value('sales_person', '');
                }
            }
        });
}


function update_tax_fields(frm) {

    if (frm.doc.docstatus === 1) return;

    if (frm.doc.order_type === "Import PI") {
               
        frm.set_value("taxes_and_charges", null);
        frm.clear_table("taxes");

        let net_total = frm.doc.net_total || 0;
        frm.set_value("total_taxes_and_charges", 0.0);
        frm.set_value("grand_total", net_total);
        frm.set_value("base_grand_total", frm.doc.base_net_total || net_total);
        
        // Hide taxes table
        frm.set_df_property("taxes", "hidden", 1);
        frm.set_df_property("total_taxes_and_charges", "hidden", 1);
        $(frm.fields_dict.base_total_taxes_and_charges.$wrapper).closest(".frappe-control").hide();  
        
    } else {
        // Show taxes table if not Import PI
        frm.set_df_property("taxes", "hidden", 0);
        frm.set_df_property("base_total_taxes_and_charges", "hidden", 0);
        $(frm.fields_dict.base_total_taxes_and_charges.$wrapper).closest(".frappe-control").show();
    }

    frm.refresh_fields(["taxes", "taxes_and_charges", "total_taxes_and_charges", "grand_total", "base_grand_total",]);
    
}


