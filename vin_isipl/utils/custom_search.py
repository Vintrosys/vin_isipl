
import frappe
import re
import frappe.desk.search

_original_search_link = frappe.desk.search.__dict__["search_link"]
build_for_autosuggest = frappe.desk.search.build_for_autosuggest

search_fields_map = {
    "Item": ["name", "item_name", "item_group"],
    "Customer": ["name", "customer_name", "customer_group"],
    "Supplier": ["name", "supplier_name", "supplier_group"]
}


def sanitize(s):
    return re.sub(r'[^a-zA-Z0-9]', '', (s or '')).lower()

# Currently search optimization done only for Item, Customer, Supplier
def before_save(doc, method):
    for field in ["item_code", "customer_name", "supplier_name"]:
        if hasattr(doc, field):
            value = getattr(doc, field)
            if value:
                doc.custom_search_key = sanitize(value)
                break

@frappe.whitelist()
def custom_search_link(
    doctype,
    txt,
    query=None,
    searchfield=None,
    page_len=20,
    start=0,
    filters=None,
    reference_doctype=None,
    ignore_user_permissions=False,
):    
    meta = frappe.get_meta(doctype)
    has_custom_search_key = any(df.fieldname == "custom_search_key" for df in meta.fields)
    has_disabled = any(df.fieldname == "disabled" and df.fieldtype == "Check" for df in meta.fields)

    where_clause = "custom_search_key LIKE %(txt)s"
    if has_disabled:
        where_clause += " AND disabled = 0"


    if not has_custom_search_key:
       
        return _original_search_link(
            doctype,
            txt,
            query=query,
            filters=filters,
            page_length=page_len,
            searchfield=searchfield,
            reference_doctype=reference_doctype,
            ignore_user_permissions=ignore_user_permissions,
        )

    clean_txt = re.sub(r"[^a-zA-Z0-9]", "", txt.lower())

    fields = search_fields_map.get(doctype, ["name"])
    field_sql = ", ".join(fields)

    results = frappe.db.sql(f"""
        SELECT {field_sql}
        FROM `tab{doctype}`
        WHERE {where_clause}
        ORDER BY modified DESC
        LIMIT %(start)s, %(page_len)s
    """, {
        "txt": f"%{clean_txt}%",
        "start": start,
        "page_len": page_len
    })


    return build_for_autosuggest(results, doctype=doctype)


