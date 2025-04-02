frappe.ui.form.on('Payment Entry', {
    onload: function (frm) {        
        frm.trigger('set_naming_series');  
    },
    company: function (frm) {
        frm.trigger('set_naming_series');
    },
    payment_type: function (frm) {
        frm.trigger('set_naming_series');
    },
    set_naming_series: function (frm) {
        const company = frm.doc.company;
        const payment_type = frm.doc.payment_type;

        if (payment_type == "Receive") {
            if (company == "INNOVATIVE SEWING INDIA PRIVATE LIMITED") {
                frm.set_value('naming_series', 'ISIPL/R/.FY.####');
            } else if (company == "INNOVATIVE") {
                frm.set_value('naming_series', 'INN/R/.FY.####');
            }

        } else if (payment_type == "Pay") {
            if (company == "INNOVATIVE SEWING INDIA PRIVATE LIMITED") {
                frm.set_value('naming_series', 'ISIPL/P/.FY.####');
            } else if (company == "INNOVATIVE") {
                frm.set_value('naming_series', 'INN/P/.FY.####');
            }

        } else if (payment_type == "Internal Transfer") {
            if (company == "INNOVATIVE SEWING INDIA PRIVATE LIMITED") {
                frm.set_value('naming_series', 'ISIPL/I/.FY.####');
            } else if (company == "INNOVATIVE") {
                frm.set_value('naming_series', 'INN/I/.FY.####');
            }
        }
    }
})

