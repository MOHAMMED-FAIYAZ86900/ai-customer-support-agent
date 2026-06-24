from fastapi import FastAPI
from pydantic import BaseModel
from backend.agent import process_customer_message

from backend.database import get_customer_by_order_id
from backend.policy_engine import check_refund_eligibility
from backend.logs import get_logs, clear_logs
from backend.agent_llm import process_with_llm
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {
        "message": "AI Refund Agent Running"
    }


@app.get("/customer/{order_id}")
def get_customer(order_id: str):

    customer = get_customer_by_order_id(order_id)

    if not customer:
        return {
            "success": False,
            "message": "Customer not found"
        }

    return {
        "success": True,
        "customer": customer
    }


@app.get("/refund/{order_id}")
def refund_check(order_id: str):

    clear_logs()

    customer = get_customer_by_order_id(order_id)

    if not customer:
        return {
            "success": False,
            "message": "Customer not found"
        }

    result = check_refund_eligibility(customer)

    return {
        "success": True,
        "order_id": order_id,
        "customer_name": customer["name"],
        "result": result
    }


@app.get("/logs")
def logs():

    return {
        "logs": get_logs()
    }

@app.post("/chat")
def chat(request: ChatRequest):

    result = process_customer_message(
        request.message
    )

    return result

@app.post("/chat-ai")
def chat_ai(request: ChatRequest):

    result = process_with_llm(
        request.message
    )

    return result