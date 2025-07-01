frappe.ui.form.on('Sales Invoice', {
    refresh: function (frm){
        if (frm.doc.name && frm.doc.creation && frm.doc.docstatus < 2) {
            frm.add_custom_button(__('Print PDF'), function () {
                let format = 'Commercial Invoice';
                let url = `/api/method/frappe.utils.print_format.download_pdf?doctype=${frm.doc.doctype}&name=${frm.doc.name}&format=${format}`;
                window.open(url, '_blank');
            });
        }
    },
    onload: function (frm) {        
        frm.trigger('set_naming_series');
        if (!frm.doc.custom_sales_person) {  
            frm.trigger('set_sales_person'); 
        }        
    },

    custom_invoice_type: function (frm) {
        frm.trigger('set_naming_series');
    },

    company: function (frm) {
        frm.trigger('set_naming_series');
        frm.trigger('set_default_wh');
    },

    is_return: function (frm) {
        frm.trigger('set_naming_series');
    },
    
    customer: function (frm) {
        frm.trigger('set_sales_person');  
    },

    // Stock update not required for spares as of now -- to be enabled from APR 2026

    custom_sales_category: function (frm) {
        if (frm.doc.custom_sales_category == "Product Sales") {
            frm.set_value('update_stock', 1);
        }
        else {
            frm.set_value('update_stock', 0);
        }
        frm.trigger('set_default_wh');
    },

    set_default_wh: function (frm) {        
        if (frm.doc.update_stock) {
            if (frm.doc.company == "ISIPL") {
                frm.set_value('set_warehouse', 'Godown - ISIPL');
            } 
            else {
                frm.set_value('set_warehouse', '');
            }    
        }
    },

    set_naming_series: function (frm) {
        const company = frm.doc.company;
        const invoice_type = frm.doc.custom_invoice_type;

        if (invoice_type == "COMMISSION") {
            frm.set_value('naming_series', 'CINV/.FY.####');
            frm.set_value('company', 'ISIPL');
            frm.set_df_property('company', 'read_only', 1);

        } else if (frm.doc.is_return) {
            if (company == "ISIPL") {
                frm.set_value('naming_series', 'ISIPL/CN/.FY.####');
            } else if (company == "INNOVATIVE") {
                frm.set_value('naming_series', 'INN/CN/.FY.####');
            }

        } else if (invoice_type == "CREDIT") {
            if (company == "ISIPL") {
                frm.set_value('naming_series', 'ISIPL/.FY.####');
            } else if (company == "INNOVATIVE") {
                frm.set_value('naming_series', 'INN/.FY.####');
            }
            frm.set_df_property('company', 'read_only', 0); 

        } else if (invoice_type == "CASH") {
            if (company == "ISIPL") {
                frm.set_value('naming_series', 'C/.FY.####');
            } else if (company == "INNOVATIVE") {
                frm.set_value('naming_series', 'INN/C/.FY.####');
            }
            frm.set_df_property('company', 'read_only', 0); 
        }
    },

    set_sales_person: function (frm) {
        if (frm.doc.customer) {
            frappe.db.get_value('CRM Deal', { organization: frm.doc.customer }, 'deal_owner')
                .then(r => {
                    if (r.message && r.message.deal_owner) {
                        fetch_sales_person(frm, r.message.deal_owner);
                    } else {
                        frappe.db.get_value('Customer', frm.doc.customer, 'custom_sales_person')
                .then(r => {
                    if (r.message && r.message.custom_sales_person) {
                        frm.set_value('custom_sales_person', r.message.custom_sales_person);
                    } else {
                        if (!frm.doc.custom_sales_person) {
                            frm.set_value('custom_sales_person', '');
                        }
                    }
                });
                    }
                });
                
        } else {
            if (!frm.doc.custom_sales_person) {
                frm.set_value('custom_sales_person', '');
            } 
        }
    }     
})

function fetch_sales_person(frm, deal_owner) {    
    frappe.db.get_value('Employee', { user_id: deal_owner }, 'name')
        .then(emp => {
            if (emp.message && emp.message.name) {               
                frappe.db.get_value('Sales Person', { employee: emp.message.name }, 'name')
                    .then(sp => {
                        if (!frm.doc.custom_sales_person) {
                            frm.set_value('custom_sales_person', sp.message.name);
                        }    

                    });
            } else {
                if (!frm.doc.custom_sales_person) {
                    frm.set_value('custom_sales_person', '');
                }
            }
        });
}