import re

from backend.openrouter_client import client
from backend.tools import refund_validation_tool
from backend.logs import clear_logs

import re


def normalize_order_id(text):

    text = text.upper()

    patterns = [
        r"ORDER\s*(\d+)",
        r"ORD\s*(\d+)",
        r"O\s*R\s*D\s*(\d+)"
    ]

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:
            return f"ORD{match.group(1)}"

    return None

def process_with_llm(user_message):
    clear_logs()

    order_id = normalize_order_id(
        user_message
    )

    if not order_id:
        return {
            "response":
            "Please provide a valid order ID."
    }

    refund_result = refund_validation_tool(order_id)

    if not refund_result["success"]:
        return {
            "response": "Customer not found."
        }

    customer = refund_result["customer"]

    decision = refund_result["result"]

    prompt = prompt = f"""
You are an AI customer support refund agent.

Rules:
- Reply in chat format.
- Maximum 40 words.
- Be concise and professional.
- Start with either:
  ✅ Refund Approved
  or
  ❌ Refund Denied
- Mention the reason.
- Never write emails.
- Never write subject lines.

Customer Name: {customer['name']}
Order ID: {order_id}

Decision:
{decision}
"""

    response = client.chat.completions.create(
        model="google/gemini-2.5-flash",
        max_tokens=200,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "response": response.choices[0].message.content
    }