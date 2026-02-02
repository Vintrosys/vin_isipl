frappe.ui.form.on('Quotation', {

    // -------------------------------
    // FILTER TERMS BY PRE SALES TYPE
    // -------------------------------
    set_tc_query: function (frm) {
        frm.set_query("tc_name", function () {
            // if (!frm.doc.order_type) {
            //     return {};
            // }

            return {
                filters: {
                    custom_pre_sales_type: frm.doc.order_type
                }
            };
        });
    },

    // FILTER PAYMENT TERMS TEMPLATE

    set_payment_terms_query: function (frm) {
        frm.set_query("payment_terms_template", function () {
            return {
                filters: {
                    custom_pre_sales_type: frm.doc.order_type
                }
            };
        });
    },

    // FILTER SHIPPING TERM

    set_shipping_term_query: function (frm) {
        frm.set_query("custom_shipping_term", function () {
            return {
                filters: {
                    custom_pre_sales_type: frm.doc.order_type
                }
            };
        });
    },

    // -------------------------------
    // REFRESH
    // -------------------------------
    refresh: function (frm) {

        // apply terms filter on load
        frm.trigger('set_tc_query');

        frm.trigger('set_payment_terms_query');

        frm.trigger('set_shipping_term_query');
        
        setTimeout(() => {
            $(frm.page.wrapper)
                .find('.btn:contains("Get Items From")')
                .remove();
        }, 5);

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

                let url =
                    `/api/method/frappe.utils.print_format.download_pdf` +
                    `?doctype=${frm.doc.doctype}` +
                    `&name=${frm.doc.name}` +
                    `&format=${format}`;

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
                        frappe.show_alert({
                            message: __("Version Tracker Updated!"),
                            indicator: 'green'
                        });
                    }
                });
            });
        }
    },

    // -------------------------------
    // PARTY NAME
    // -------------------------------
    party_name: function (frm) {
        frm.set_value('sales_person', '');
        frm.trigger('set_party_name');
    },

    // -------------------------------
    // PRE SALES TYPE
    // -------------------------------
    order_type: function (frm) {

        if (frm.doc.order_type === "Import PI" || frm.doc.order_type === "Stock PI") {
            frm.set_value('company', 'ISIPL');
        } else if (frm.doc.order_type === "Spares PI" || frm.doc.order_type === "Service PI") {
            frm.set_value('company', 'INNOVATIVE');
        }

        setTimeout(() => {

            if (frm.doc.order_type === "Import PI") {
                frm.set_value('currency', 'USD');
                frm.set_value('tax_category', 'Nil Tax');
                frm.set_df_property('tc_name', 'reqd', 0);
                frm.set_df_property('tc_name', 'hidden', 1);
                frm.set_value('tc_name', '');
            } else {
                frm.set_value('currency', 'INR');
                frm.set_df_property('tc_name', 'reqd', 1);
                frm.set_df_property('tc_name', 'hidden', 0);
            }

             // re-apply filters
            frm.trigger('set_tc_query');
            frm.trigger('set_payment_terms_query');
            frm.trigger('set_shipping_term_query');

            // clear old values to avoid mismatch
            frm.set_value('tc_name', '');
            frm.set_value('payment_terms_template', '');
            frm.set_value('custom_shipping_term', '');

        }, 300);

        frm.trigger('party_name');
    },

    // -------------------------------
    // COMPANY
    // -------------------------------
    // company: function (frm) {

    //     if (frm.doc.company === "ISIPL") {
    //         frm.set_value('naming_series', 'ISIPL-TPR-.FY.####');
    //         frm.set_value('tc_name', '');
    //         frm.set_value('custom_isipl_bank_account', '');
    //         frm.set_value('payment_terms_template', '');
    //         frm.set_value('custom_shipping_term', '');

    //     } else if (frm.doc.company === "INNOVATIVE") {
    //         frm.set_value('naming_series', 'INN-TPR-.FY.####');
    //         frm.set_value('custom_isipl_bank_account', 'Innovative - IndusInd Bank');
    //         frm.set_value('payment_terms_template', 'Immediate');
    //         frm.set_value('custom_shipping_term', 'Ex - Works Tirupur');

    //         if (frm.doc.order_type === "Service PI") {
    //             frm.set_value('tc_name', 'Terms and Conditions - SERVICE AMC');
    //         } else {
    //             frm.set_value('tc_name', 'Terms and Conditions - STANDARD');
    //         }
    //     }
    // },

    // -------------------------------
    // SET TERMS DEFAULT
    // -------------------------------
    // set_terms: function (frm) {

    //     if (frm.doc.company === "ISIPL") {
    //         frm.set_value('tc_name', '');
    //     } 
    //     else {
    //         if (frm.doc.order_type === "Service PI") {
    //             frm.set_value('tc_name', 'Terms and Conditions - SERVICE AMC');
    //         } else {
    //             frm.set_value('tc_name', 'Terms and Conditions - STANDARD');
    //         }
    //     }
    // },

    // -------------------------------
    // SET PARTY NAME
    // -------------------------------
    set_party_name: function (frm) {

        if (frm.doc.party_name) {

            frappe.db.get_value(
                'CRM Deal',
                { organization: frm.doc.party_name },
                'custom_sales_person'
            ).then(r => {
                if (r.message && r.message.custom_sales_person) {
                    fetch_sales_person(frm, r.message.custom_sales_person);
                } else if (!frm.doc.sales_person) {
                    frm.set_value('sales_person', '');
                }
            });

            frappe.db.get_value(
                'Customer',
                frm.doc.party_name,
                'custom_sales_person'
            ).then(r => {
                if (r.message && r.message.custom_sales_person) {
                    frm.set_value('sales_person', r.message.custom_sales_person);
                } else if (!frm.doc.sales_person) {
                    frm.set_value('sales_person', '');
                }
            });

        } else if (!frm.doc.sales_person) {
            frm.set_value('sales_person', '');
        }
    }
});

// -------------------------------
// FETCH SALES PERSON
// -------------------------------
function fetch_sales_person(frm, sales_person) {

    frappe.db.get_value(
        'Employee',
        { user_id: sales_person },
        'name'
    ).then(emp => {

        if (emp.message && emp.message.name) {

            frappe.db.get_value(
                'Sales Person',
                { employee: emp.message.name },
                'name'
            ).then(sp => {
                if (!frm.doc.sales_person && sp.message) {
                    frm.set_value('sales_person', sp.message.name);
                }
            });

        } else if (!frm.doc.sales_person) {
            frm.set_value('sales_person', '');
        }
    });
}
