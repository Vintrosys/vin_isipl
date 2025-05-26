frappe.provide("erpnext");
frappe.provide("erpnext.utils");
frappe.provide("erpnext.stock.utils");

erpnext.utils.update_child_items = function (opts) {
	const frm = opts.frm;
	const cannot_add_row = typeof opts.cannot_add_row === "undefined" ? true : opts.cannot_add_row;
	const child_docname = typeof opts.cannot_add_row === "undefined" ? "items" : opts.child_docname;
	const child_meta = frappe.get_meta(`${frm.doc.doctype} Item`);
	const has_reserved_stock = opts.has_reserved_stock ? true : false;
	const get_precision = (fieldname) => child_meta.fields.find((f) => f.fieldname == fieldname).precision;

	this.data = frm.doc[opts.child_docname].map((d) => {
		return {
			docname: d.name,
			name: d.name,
			item_code: d.item_code,
			delivery_date: d.delivery_date,
			schedule_date: d.schedule_date,
			conversion_factor: d.conversion_factor,
			qty: d.qty,
			rate: d.rate,
			uom: d.uom,
			fg_item: d.fg_item,
			fg_item_qty: d.fg_item_qty,
			warehouse: d.warehouse,
			discount_percentage: d.discount_percentage,
			amount: d.amount,
			item_tax_template: d.item_tax_template,
			price_list_rate: d.price_list_rate
		};
	});

	const fields = [
		{
			fieldtype: "Data",
			fieldname: "docname",
			read_only: 1,
			hidden: 1,
		},
		{
			fieldtype: "Link",
			fieldname: "item_code",
			options: "Item",
			in_list_view: 1,
			read_only: 0,
			disabled: 0,
			label: __("Item Code"),
			get_query: function () {
				let filters;
				if (frm.doc.doctype == "Sales Order") {
					filters = { is_sales_item: 1 };
				} else if (frm.doc.doctype == "Purchase Order") {
					if (frm.doc.is_subcontracted) {
						if (frm.doc.is_old_subcontracting_flow) {
							filters = { is_sub_contracted_item: 1 };
						} else {
							filters = { is_stock_item: 0 };
						}
					} else {
						filters = { is_purchase_item: 1 };
					}
				}
				return {
					query: "erpnext.controllers.queries.item_query",
					filters: filters,
				};
			},
			onchange: function () {
				const me = this;

				frm.call({
					method: "erpnext.stock.get_item_details.get_item_details",
					args: {
						doc: frm.doc,
						args: {
							item_code: this.value,
							set_warehouse: frm.doc.set_warehouse,
							customer: frm.doc.customer || frm.doc.party_name,
							quotation_to: frm.doc.quotation_to,
							supplier: frm.doc.supplier,
							currency: frm.doc.currency,
							is_internal_supplier: frm.doc.is_internal_supplier,
							is_internal_customer: frm.doc.is_internal_customer,
							conversion_rate: frm.doc.conversion_rate,
							price_list: frm.doc.selling_price_list || frm.doc.buying_price_list,
							price_list_currency: frm.doc.price_list_currency,
							plc_conversion_rate: frm.doc.plc_conversion_rate,
							company: frm.doc.company,
							order_type: frm.doc.order_type,
							is_pos: cint(frm.doc.is_pos),
							is_return: cint(frm.doc.is_return),
							is_subcontracted: frm.doc.is_subcontracted,
							ignore_pricing_rule: frm.doc.ignore_pricing_rule,
							doctype: frm.doc.doctype,
							name: frm.doc.name,
							qty: me.doc.qty || 1,
							uom: me.doc.uom,
							pos_profile: cint(frm.doc.is_pos) ? frm.doc.pos_profile : "",
							tax_category: frm.doc.tax_category,
							child_doctype: frm.doc.doctype + " Item",
							is_old_subcontracting_flow: frm.doc.is_old_subcontracting_flow,
							discount_percentage: me.doc.discount_percentage,
							amount: me.doc.amount,
							item_tax_template: me.doc.item_tax_template,
							price_list_rate: me.doc.price_list_rate
						},
					},
					callback: function (r) {
						if (r.message) {
							const { qty, price_list_rate: rate, uom, conversion_factor, bom_no, discount_percentage, warehouse, price_list_rate} = r.message;

							const row = dialog.fields_dict.trans_items.df.data.find(
								(doc) => doc.idx == me.doc.idx
							);
							if (row) {
								Object.assign(row, {
									conversion_factor: me.doc.conversion_factor || conversion_factor,
									uom: me.doc.uom || uom,
									qty: me.doc.qty || qty,
									rate: me.doc.rate || rate,
									bom_no: bom_no,
									discount_percentage: me.doc.discount_percentage || discount_percentage,
									warehouse: me.doc.warehouse || warehouse,
									price_list_rate: me.doc.price_list_rate || price_list_rate
								});
								dialog.fields_dict.trans_items.grid.refresh();
							}
						}
					},
				});
			},
		},
		{
			fieldtype: "Link",
			fieldname: "uom",
			options: "UOM",
			read_only: 0,
			label: __("UOM"),
			reqd: 1,
			onchange: function () {
				frappe.call({
					method: "erpnext.stock.get_item_details.get_conversion_factor",
					args: { item_code: this.doc.item_code, uom: this.value },
					callback: (r) => {
						if (!r.exc) {
							if (this.doc.conversion_factor == r.message.conversion_factor) return;

							const docname = this.doc.docname;
							dialog.fields_dict.trans_items.df.data.some((doc) => {
								if (doc.docname == docname) {
									doc.conversion_factor = r.message.conversion_factor;
									dialog.fields_dict.trans_items.grid.refresh();
									return true;
								}
							});
						}
					},
				});
			},
		},
		{
			fieldtype: "Float",
			fieldname: "qty",
			default: 0,
			read_only: 0,
			in_list_view: 1,
			label: __("Qty"),
			precision: get_precision("qty"),
		},
		{
			fieldtype: "Currency",
			fieldname: "rate",
			options: "currency",
			default: 0,
			read_only: 1,
			in_list_view: 1,
			label: __("Rate"),
			precision: get_precision("rate"),
		},			
	];

	// Additional fields added here
    if (frm.doc.doctype == "Purchase Order") {
        fields.push(
			
			{
				fieldtype: "Currency",
				fieldname: "price_list_rate",
				options: "currency",
				default: 0,
				read_only: 0,
				in_list_view: 1,
				label: __("Price List Rate"),
				precision: get_precision("price_list_rate"),
			},	
			{
				fieldtype: "Percent",
				fieldname: "discount_percentage",
				default: 0,
				read_only: 0,
				in_list_view: 1,
				label: __("Discount"),
			},
			{
				fieldtype: "Currency",
				fieldname: "amount",
				default: 0,
				read_only: 1,
				in_list_view: 1,
				label: __("Amount"),
			},
			{
				fieldtype: "Link",
				fieldname: "item_tax_template",
				options: "Item Tax Template",
				read_only: 0,
				in_list_view: 1,
				label: __("Item Tax Template"),
				get_query: () => {
					let company = cur_frm.doc.company;
					return {
						filters: {
							company: company
						}
					};
				}
			}
        );
    }

	if (frm.doc.doctype == "Purchase Order") {
		fields.splice(3, 0, {
			fieldtype: "Float",
			fieldname: "conversion_factor",
			label: __("Conversion Factor"),
			precision: get_precision("conversion_factor"),
		});
	}

	if (
		frm.doc.doctype == "Purchase Order" &&
		frm.doc.is_subcontracted &&
		!frm.doc.is_old_subcontracting_flow
	) {
		fields.push(
			{
				fieldtype: "Link",
				fieldname: "fg_item",
				options: "Item",
				reqd: 1,
				in_list_view: 0,
				read_only: 0,
				disabled: 0,
				label: __("Finished Good Item"),
				get_query: () => {
					return {
						filters: {
							is_stock_item: 1,
							is_sub_contracted_item: 1,
							default_bom: ["!=", ""],
						},
					};
				},
			},
			{
				fieldtype: "Float",
				fieldname: "fg_item_qty",
				reqd: 1,
				default: 0,
				read_only: 0,
				in_list_view: 0,
				label: __("Finished Good Item Qty"),
				precision: get_precision("fg_item_qty"),
			}
		);
	}

	let dialog = new frappe.ui.Dialog({
		title: __("Update Items"),
		size: "extra-large",
		fields: [
			{
				fieldname: "trans_items",
				fieldtype: "Table",
				label: "Items",
				cannot_add_rows: cannot_add_row,
				in_place_edit: false,
				reqd: 1,
				data: this.data,
				get_data: () => {
					return this.data;
				},
				fields: fields,
			},
		],
		primary_action: function () {
			if (frm.doctype == "Sales Order" && has_reserved_stock) {
				this.hide();
				frappe.confirm(
					__(
						"The reserved stock will be released when you update items. Are you certain you wish to proceed?"
					),
					() => this.update_items()
				);
			} else {
				this.update_items();
			}
		},
		update_items: function () {
			const trans_items = this.get_values()["trans_items"].filter((item) => !!item.item_code);
			
			frappe.call({
				method: "erpnext.controllers.accounts_controller.update_child_qty_rate",
				freeze: true,
				args: {
					parent_doctype: frm.doc.doctype,
					trans_items: trans_items,
					parent_doctype_name: frm.doc.name,
					child_docname: child_docname,
				},
				callback: function () {
					frm.reload_doc();					
				},
			});
			this.hide();
			refresh_field("items");
		},
		primary_action_label: __("Update"),
	});

	dialog.show();
};