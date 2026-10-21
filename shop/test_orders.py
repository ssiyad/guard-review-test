from unittest.mock import MagicMock, patch

from shop import orders


@patch("shop.orders.get_customer", return_value=MagicMock(name="cust"))
@patch("shop.orders.frappe")
def test_discount_is_applied_and_stored(frappe, _customer):
    frappe.db.get_value.return_value = 10
    orders.place_order("C1", [{"qty": 2, "rate": 50}], "SAVE10")
    doc = frappe.get_doc.call_args.args[0]
    assert doc["grand_total"] == 90
    assert doc["discount_code"] == "SAVE10"


@patch("shop.orders.get_customer", return_value=MagicMock(name="cust"))
@patch("shop.orders.frappe")
def test_unknown_code_is_rejected(frappe, _customer):
    frappe.db.get_value.return_value = None
    frappe.throw.side_effect = ValueError
    try:
        orders.place_order("C1", [{"qty": 1, "rate": 10}], "NOPE")
    except ValueError:
        return
    raise AssertionError("expected an error")


@patch("shop.orders.get_customer", return_value=MagicMock(name="cust"))
@patch("shop.orders.frappe")
def test_no_code_keeps_total(frappe, _customer):
    orders.place_order("C1", [{"qty": 1, "rate": 10}])
    assert frappe.get_doc.call_args.args[0]["grand_total"] == 10
