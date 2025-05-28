frappe.ui.form.on('Purchase Receipt', {    
    refresh: function (frm){
        if (!frm.is_new()) {    
            frm.add_custom_button(__('Print PDF'), function () {
                let format = 'ISIPL GRN';
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
    },
    set_naming_series: function (frm) {
        const company = frm.doc.company;
        if (frm.doc.is_return) {
            if (company == "ISIPL") {
                frm.set_value('naming_series', 'ISIPL/PR/.FY.####');
            } else if (company == "INNOVATIVE") {
                frm.set_value('naming_series', 'INN/PR/.FY.####');
            }
            frm.refresh_field("naming_series");
        }
        else{
        if (company == "ISIPL") {
            frm.set_value('naming_series', 'ISIPL/GRN/.FY.####');
        } else if (company == "INNOVATIVE") {
            frm.set_value('naming_series', 'INN/GRN/.FY.####');
        }
    }
    }
})
