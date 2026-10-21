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
    frappe.throw.side_effect = ValueError("invalid code")
    try:
        orders.place_order("C1", [{"qty": 1, "rate": 10}], "NOPE")
    except ValueError as error:
        assert str(error) == "invalid code"
        frappe.get_doc.assert_not_called()
        return
    raise AssertionError("expected an error")


@patch("shop.orders.get_customer", return_value=MagicMock(name="cust"))
@patch("shop.orders.frappe")
def test_no_code_keeps_total(frappe, _customer):
    orders.place_order("C1", [{"qty": 1, "rate": 10}])
    assert frappe.get_doc.call_args.args[0]["grand_total"] == 10


@patch("shop.orders.place_order", return_value="SO-1")
@patch("shop.orders.frappe")
def test_create_order_passes_the_code(frappe, place_order):
    frappe.parse_json.side_effect = lambda value: value
    assert orders.create_order("C1", [{"qty": 1, "rate": 10}], "SAVE10") == "SO-1"
    frappe.has_permission.assert_called_once_with("Sales Order", "create", throw=True)
    place_order.assert_called_once_with("C1", [{"qty": 1, "rate": 10}], "SAVE10")
