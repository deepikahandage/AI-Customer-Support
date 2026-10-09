from fastapi import FastAPI
from pydantic import BaseModel

from workflow import run_customer_workflow


app = FastAPI(
    title="AI Customer Support API",
    description="Multi-Agent AI Customer Support and Decision Engine",
    version="1.0.0"
)


class CustomerRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "message": "AI Customer Support API is running",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/agents")
def get_agents():
    return {
        "agents": [
            "Supervisor Agent",
            "Order Agent",
            "Refund & Return Agent",
            "Technical Support Agent",
            "Product Agent",
            "Business Agent"
        ]
    }


@app.post("/chat")
def chat(request: CustomerRequest):

    response = run_customer_workflow(request.message)

    return {
        "customer_message": request.message,
        "response": response
    }