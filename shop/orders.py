import frappe


def get_customer(customer_id):
    return frappe.get_doc("Customer", customer_id)


def place_order(customer_id, items, discount_code=None):
    customer = get_customer(customer_id)
    total = sum(item["qty"] * item["rate"] for item in items)
    if discount_code:
        percent = frappe.db.get_value("Discount Code", discount_code, "percent")
        if percent is None:
            frappe.throw(f"Discount code {discount_code} is not valid")
        total = total - total * percent / 100
    order = frappe.get_doc({"doctype": "Sales Order", "customer": customer.name, "grand_total": total})
    order.insert()
    return order.name


@frappe.whitelist()
def create_order(customer_id, items, discount_code=None):
    frappe.has_permission("Sales Order", "create", throw=True)
    return place_order(customer_id, frappe.parse_json(items), discount_code)
