frappe.ui.form.on('Item', {
    refresh: function (frm) {        
        frm.set_query('custom_isipl_item_type', function () {
            return {
                filters: [
                    ['Item Group', 'is_group', '=', 0],
                    ['Item Group', 'parent_item_group', '=', 'All Item Groups']
                ]
            };
        });

        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Item Group',
                filters: {
                    is_group: 0,
                    parent_item_group: 'All Item Groups'
                },
                fields: ['name']  
            },
            callback: function (response) {
                const item_type_groups = response.message.map(row => row.name);

                frm.set_query('item_group', function () {
                    return {
                        filters: [
                            ['Item Group', 'name', 'not in', item_type_groups]
                            
                        ]
                    };
                });
            }
        });
    }
});
