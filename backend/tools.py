from backend.database import get_customer_by_order_id
from backend.policy_engine import check_refund_eligibility


def lookup_customer_tool(order_id):

    customer = get_customer_by_order_id(order_id)

    return customer


def refund_validation_tool(order_id):

    customer = get_customer_by_order_id(order_id)

    if not customer:
        return {
            "success": False,
            "message": "Customer not found"
        }

    result = check_refund_eligibility(customer)

    return {
        "success": True,
        "customer": customer,
        "result": result
    }