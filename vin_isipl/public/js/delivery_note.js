frappe.ui.form.on('Delivery Note', {
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
                frm.set_value('naming_series', 'ISIPL/SR/.FY.####');
            } else if (company == "INNOVATIVE") {
                frm.set_value('naming_series', 'INN/SR/.FY.####');
            }
            frm.refresh_field("naming_series");
        }
        else{
        if (company == "ISIPL") {
            frm.set_value('naming_series', 'ISIPL/DC/.FY.####');
        } else if (company == "INNOVATIVE") {
            frm.set_value('naming_series', 'INN/DC/.FY.####');
        }
    }
    }
})
