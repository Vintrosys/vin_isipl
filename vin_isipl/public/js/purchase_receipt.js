frappe.ui.form.on('Purchase Receipt', {
    onload: function (frm) {        
        frm.trigger('set_naming_series');  
    },
    company: function (frm) {
        frm.trigger('set_naming_series');
    },
    set_naming_series: function (frm) {
        const company = frm.doc.company;
        if (frm.doc.is_return) {
            if (company == "INNOVATIVE SEWING INDIA PRIVATE LIMITED") {
                frm.set_value('naming_series', 'ISIPL/PR/.FY.####');
            } else if (company == "INNOVATIVE") {
                frm.set_value('naming_series', 'INN/PR/.FY.####');
            }
            frm.refresh_field("naming_series");
        }
        else{
        if (company == "INNOVATIVE SEWING INDIA PRIVATE LIMITED") {
            frm.set_value('naming_series', 'ISIPL/GRN/.FY.####');
        } else if (company == "INNOVATIVE") {
            frm.set_value('naming_series', 'INN/GRN/.FY.####');
        }
    }
    }
})
