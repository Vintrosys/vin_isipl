frappe.listview_settings['HD Ticket'] = {
    formatters: {
        // ---------- Priority ----------
        priority(value) {
            let color = 'gray';

            if (value === 'High') color = 'red';
            else if (value === 'Medium') color = 'orange';
            else if (value === 'Low') color = 'green';
            else if (value === 'Urgent') color = 'purple';

            return `<span style="color:${color}; font-weight:600;">${value || ''}</span>`;
        },

        // ---------- Status ----------
        status(value) {
            let color = 'gray';

            if (value === 'Open') color = 'red';
            else if (value === 'Assigned') color = 'blue';
            else if (value === 'Working') color = 'orange';
            else if (value === 'Pending') color = 'goldenrod';
            else if (value === 'Resolved') color = 'green';
            else if (value === 'Closed') color = 'gray';
            else if (value === 'Cancelled') color = 'darkgray';

            return `<span style="color:${color}; font-weight:600;">${value || ''}</span>`;
        }
    }
};
