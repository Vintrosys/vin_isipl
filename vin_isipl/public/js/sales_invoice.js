frappe.ui.form.on('Sales Invoice', {
    
    onload: function (frm) {        
        frm.trigger('set_naming_series');  
    },

    refresh: function (frm) {         
        frm.trigger('set_sales_person');  
    },

    custom_invoice_type: function (frm) {
        frm.trigger('set_naming_series');
    },

    company: function (frm) {
        frm.trigger('set_naming_series');
    },

    is_return: function (frm) {
        frm.trigger('set_naming_series');
    },

    customer: function (frm) {
        frm.trigger('set_sales_person');  
    },

    set_naming_series: function (frm) {
        const company = frm.doc.company;
        const invoice_type = frm.doc.custom_invoice_type;

        if (invoice_type == "COMMISSION") {
            frm.set_value('naming_series', 'CINV/.FY.####');
            frm.set_value('company', 'INNOVATIVE SEWING INDIA PRIVATE LIMITED');
            frm.set_df_property('company', 'read_only', 1);

        } else if (frm.doc.is_return) {
            if (company == "INNOVATIVE SEWING INDIA PRIVATE LIMITED") {
                frm.set_value('naming_series', 'ISIPL/CN/.FY.####');
            } else if (company == "INNOVATIVE") {
                frm.set_value('naming_series', 'INN/CN/.FY.####');
            }

        } else if (invoice_type == "CREDIT") {
            if (company == "INNOVATIVE SEWING INDIA PRIVATE LIMITED") {
                frm.set_value('naming_series', 'ISIPL/.FY.####');
            } else if (company == "INNOVATIVE") {
                frm.set_value('naming_series', 'INN/.FY.####');
            }
            frm.set_df_property('company', 'read_only', 0); 

        } else if (invoice_type == "CASH") {
            if (company == "INNOVATIVE SEWING INDIA PRIVATE LIMITED") {
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
                        frm.set_value('custom_sales_person', '');
                    }
                });
        } else {
            frm.set_value('custom_sales_person', '');  
        }
    }     
})

function fetch_sales_person(frm, deal_owner) {    
    frappe.db.get_value('Employee', { user_id: deal_owner }, 'name')
        .then(emp => {
            if (emp.message && emp.message.name) {               
                frappe.db.get_value('Sales Person', { employee: emp.message.name }, 'name')
                    .then(sp => {
                        frm.set_value('custom_sales_person', sp.message.name);
                    });
            } else {
                frm.set_value('custom_sales_person', '');
            }
        });
}