import os
import google.generativeai as genai

from tools.refund_tools import (
    check_return_eligibility,
    check_refund_status,
    create_return_request
)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3.6-flash")


REFUND_AGENT_PROMPT = """
You are a Refund and Return Agent.

Your responsibility is to help customers with:
- Product returns
- Refund status
- Return eligibility

Use refund tools when required.
Never invent refund information.
"""


def refund_agent(user_message):

    order_id = None

    for id in ["1001", "1002", "1003"]:
        if id in user_message:
            order_id = id
            break

    if not order_id:
        return "Please provide your order ID."

    if "status" in user_message.lower():
        result = check_refund_status(order_id)

    elif "return" in user_message.lower():
        result = check_return_eligibility(order_id)

    else:
        result = check_refund_status(order_id)

    prompt = f"""
    {REFUND_AGENT_PROMPT}

    Customer:
    {user_message}

    Tool result:
    {result}

    Provide a helpful response.
    """

    response = model.generate_content(prompt)

    return response.text