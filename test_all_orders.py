import json
from backend.policy_engine import check_refund_eligibility

with open("backend/customers.json", "r") as f:
    customers = json.load(f)

approved = []
denied = []

for customer in customers:

    result = check_refund_eligibility(customer)

    if result["approved"]:
        approved.append(customer["order_id"])
    else:
        denied.append(customer["order_id"])

print("\nAPPROVED:")
print(approved)

print("\nDENIED:")
print(denied)

print("\nTOTAL APPROVED:", len(approved))
print("TOTAL DENIED:", len(denied))