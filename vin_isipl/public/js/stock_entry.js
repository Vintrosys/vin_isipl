frappe.ui.form.on('Stock Entry', {
    onload: function (frm) {        
        frm.trigger('set_naming_series');  
    },
    company: function (frm) {
        frm.trigger('set_naming_series');
    },
    set_naming_series: function (frm) {
        const company = frm.doc.company;
        if (company == "ISIPL") {
            frm.set_value('naming_series', 'ISIPL/SE/.FY.####');
        } else if (company == "INNOVATIVE") {
            frm.set_value('naming_series', 'INN/SE/.FY.####');
        }
    }
})
