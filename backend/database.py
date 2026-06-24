import json
from pathlib import Path


CUSTOMERS_FILE = Path(__file__).parent / "customers.json"


def load_customers():
    with open(CUSTOMERS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_customer_by_order_id(order_id):
    customers = load_customers()

    for customer in customers:
        if customer["order_id"] == order_id:
            return customer

    return None

if __name__ == "__main__":
    customer = get_customer_by_order_id("ORD1001")

    print(customer)