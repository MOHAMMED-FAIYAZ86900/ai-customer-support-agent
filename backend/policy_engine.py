from datetime import datetime
from backend.logs import add_log


def check_refund_eligibility(customer):

    add_log(
        "Starting refund policy validation",
        "running"
    )

    # Rule 1: Fraudulent Order
    if customer.get("fraudulent"):

        add_log(
            "Fraud Check",
            "failed"
        )

        return {
            "approved": False,
            "reason": "Fraudulent orders are not eligible for refunds."
        }

    add_log(
        "Fraud Check",
        "passed"
    )

    # Rule 2: Product Not Delivered
    if not customer.get("delivered"):

        add_log(
            "Delivery Check",
            "failed"
        )

        return {
            "approved": False,
            "reason": "Product has not been delivered."
        }

    add_log(
        "Delivery Check",
        "passed"
    )

    # Rule 3: Already Refunded
    if customer.get("refund_used"):

        add_log(
            "Refund Usage Check",
            "failed"
        )

        return {
            "approved": False,
            "reason": "Refund has already been used for this order."
        }

    add_log(
        "Refund Usage Check",
        "passed"
    )

    # Rule 4: Digital Product
    digital_products = [
        "Digital Course",
        "Ebook"
    ]

    if customer.get("product") in digital_products:

        add_log(
            "Digital Product Check",
            "failed"
        )

        return {
            "approved": False,
            "reason": "Digital products are non-refundable."
        }

    add_log(
        "Digital Product Check",
        "passed"
    )

    # Rule 5: Amount Limit
    if customer.get("amount", 0) > 1000:

        add_log(
            "Amount Limit Check",
            "failed"
        )

        return {
            "approved": False,
            "reason": "Refund amount exceeds policy limit."
        }

    add_log(
        "Amount Limit Check",
        "passed"
    )

    # Rule 6: Refund Window

    add_log(
        "Refund Window Check",
        "running"
    )

    purchase_date = datetime.strptime(
        customer["purchase_date"],
        "%Y-%m-%d"
    )

    today = datetime.today()

    days_difference = (
        today - purchase_date
    ).days

    if days_difference > 30:

        add_log(
            "Refund Window Check",
            "failed"
        )

        return {
            "approved": False,
            "reason": "Refund request is outside the 30-day window."
        }

    add_log(
        "Refund Window Check",
        "passed"
    )

    add_log(
        "Final Decision",
        "approved"
    )

    return {
        "approved": True,
        "reason": "Refund approved."
    }