import re

from backend.logs import clear_logs
from backend.tools import refund_validation_tool
from backend.logs import clear_logs


def process_customer_message(message):

    clear_logs()

    order_pattern = r"ORD\d+"

    match = re.search(order_pattern, message)

    if not match:
        return {
            "response": "Please provide a valid order ID."
        }

    order_id = match.group()

    refund_result = refund_validation_tool(order_id)

    if not refund_result["success"]:
        return {
            "response": "Customer not found."
        }

    customer = refund_result["customer"]

    decision = refund_result["result"]

    if decision["approved"]:

        return {
            "response": (
                f"Refund approved for "
                f"{customer['name']} "
                f"(Order {order_id}). "
                f"{decision['reason']}"
            )
        }

    return {
        "response": (
            f"Refund denied for "
            f"{customer['name']} "
            f"(Order {order_id}). "
            f"{decision['reason']}"
        )
    }