frappe.listview_settings['Sales Invoice'] = {
    formatters: {
        custom_print_pdf(value, doc) {
            if (value) {
                return `
                    <div style="text-align: center;">
                        <a href="${value}" target="_blank" title="View PDF" onclick="event.stopPropagation();">
                            <i class="fa fa-file-pdf-o" style="font-size: 16px; color: #d9534f;"></i>
                        </a>
                    </div>`;
            } else {
                return '';
            }
        }
    }
};
