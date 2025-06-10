frappe.ui.form.on('Purchase Receipt', {    
    refresh: function (frm){
        if (frm.doc.name && frm.doc.creation && frm.doc.docstatus < 2) {  
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

    validate: function(frm) {
        let has_error = false;

        frm.doc.items.forEach((item, i) => {
            if (flt(item.custom_total_qty) < flt(item.qty)) {
                frappe.msgprint(
                    `Row ${item.idx}: Total Qty cannot be less than Accepted Qty`
                );
                has_error = true;
            }
        });

        if (has_error) {
            frappe.validated = false;  
        }
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

frappe.ui.form.on('Purchase Receipt Item', {
    custom_total_qty(frm, cdt, cdn) {
        calculate_balance_qty(cdt, cdn);
    },
    qty(frm, cdt, cdn) {
        calculate_balance_qty(cdt, cdn);
    }
});

let qty_validation_flag = false;  

function calculate_balance_qty(cdt, cdn) {
    let item = locals[cdt][cdn];
    let total = flt(item.custom_total_qty);
    let accepted = flt(item.qty);
    let balance = total - accepted;

    frappe.model.set_value(cdt, cdn, 'custom_balance_quantity', balance);
}
