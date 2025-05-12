frappe.ui.form.on('Purchase Order', {
    onload: function (frm) {        
        frm.trigger('set_naming_series');  
    },
    company: function (frm) {
        frm.trigger('set_naming_series');
        if (frm.doc.company == "INNOVATIVE") {
            frm.set_value('set_warehouse', 'Stores - INN');
            frm.set_value('payment_terms_template', 'Immediate');
        }
    },
    set_naming_series: function (frm) {
        const company = frm.doc.company;
        if (company == "INNOVATIVE SEWING INDIA PRIVATE LIMITED") {
            frm.set_value('naming_series', 'ISIPL/PO/.FY.####');
        } else if (company == "INNOVATIVE") {
            frm.set_value('naming_series', 'INN/PO/.FY.####');
        }
    }
})
