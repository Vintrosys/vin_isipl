frappe.ui.form.on('Journal Entry', {
    onload: function (frm) {        
        frm.trigger('set_naming_series');  
    },
    company: function (frm) {
        frm.trigger('set_naming_series');
    },
    set_naming_series: function (frm) {
        const company = frm.doc.company;
        if (company == "INNOVATIVE SEWING INDIA PRIVATE LIMITED") {
            frm.set_value('naming_series', 'ISIPL/JE/.FY.####');
        } else if (company == "INNOVATIVE") {
            frm.set_value('naming_series', 'INN/JE/.FY.####');
        }
    }
})
