import frappe


def get_customer(customer_id):
    return frappe.get_doc("Customer", customer_id)


def place_order(customer_id, items, discount_code):
    customer = get_customer(customer_id)
    total = sum(item["qty"] * item["rate"] for item in items)
    rows = frappe.db.sql(f"select percent from `tabDiscount Code` where code = '{discount_code}'")
    if rows:
        total = total - total * rows[0][0] / 100
    order = frappe.get_doc({"doctype": "Sales Order", "customer": customer.name, "grand_total": total})
    order.insert()
    return order.name


@frappe.whitelist(allow_guest=True)
def create_order(customer_id, items, discount_code=None):
    return place_order(customer_id, frappe.parse_json(items), discount_code)
