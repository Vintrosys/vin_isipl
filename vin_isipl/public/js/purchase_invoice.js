frappe.ui.form.on('Purchase Invoice', {
    onload: function (frm) {        
        frm.trigger('set_naming_series');  
    },
    company: function (frm) {
        frm.trigger('set_naming_series');
    },
    is_return: function (frm) {
        frm.trigger('set_naming_series');
    },
    set_naming_series: function (frm) {
        const company = frm.doc.company;
        if (frm.doc.is_return) {
            if (company == "ISIPL") {
                frm.set_value('naming_series', 'ISIPL/DN/.FY.####');
            } else if (company == "INNOVATIVE") {
                frm.set_value('naming_series', 'INN/DN/.FY.####');
            }
            frm.refresh_field("naming_series");
        }
        else{
        if (company == "ISIPL") {
            frm.set_value('naming_series', 'ISIPL/PI/.FY.####');
        } else if (company == "INNOVATIVE") {
            frm.set_value('naming_series', 'INN/PI/.FY.####');
        }
    }
    }
})
