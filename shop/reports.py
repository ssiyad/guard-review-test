import frappe

from shop.orders import place_order


def reorder_last(customer_id):
    last = frappe.get_last_doc("Sales Order", filters={"customer": customer_id})
    items = [{"qty": i.qty, "rate": i.rate} for i in last.items]
    return place_order(customer_id, items)
