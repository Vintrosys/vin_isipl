frappe.ui.form.on('Purchase Order', {
    refresh: function (frm) {
        if (frm.doc.name && frm.doc.creation && frm.doc.docstatus < 2) {  
            frm.add_custom_button(__('Print PDF'), function () {
                let format = '';

                switch (frm.doc.company) {
                    case 'INNOVATIVE':
                        format = 'Spare PO';
                        break;
                    case 'ISIPL':
                        format = 'ISIPL PO';
                        break;
                }

                let url = `/api/method/frappe.utils.print_format.download_pdf?doctype=${frm.doc.doctype}&name=${frm.doc.name}&format=${format}`;
                window.open(url, '_blank');
            });
        }
    },

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
        if (company == "ISIPL") {
            frm.set_value('naming_series', 'ISIPL/PO/.FY.####');
        } else if (company == "INNOVATIVE") {
            frm.set_value('naming_series', 'INN/PO/.FY.####');
        }
    }
})
