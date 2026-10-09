import os
import re
import time

from dotenv import load_dotenv
from google import genai

from tools.order_tools import get_order_status


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found. Check your .env file."
    )

client = genai.Client(api_key=api_key)


# ============================================================
# ORDER AGENT PROMPT
# ============================================================

ORDER_AGENT_PROMPT = """
You are an Order Support Agent in a multi-agent AI customer
support system.

Your responsibilities are:

1. Order status
2. Delivery information
3. Tracking information
4. Basic order-related questions

Rules:

- Use the order tool information provided.
- Never invent order information.
- Do not process refunds.
- If the customer asks for a refund, explain that the
  Refund and Return Agent handles refunds.
- Be polite, concise and helpful.
"""


# ============================================================
# EXTRACT ORDER ID
# ============================================================

def extract_order_id(user_message):

    # First look for formats such as:
    # 1001
    # ORD1001
    # order 1001

    match = re.search(
        r"(?:order\s*|ord\s*)?(\d{4})",
        user_message,
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    return None


# ============================================================
# GENERATE GEMINI RESPONSE
# ============================================================

def generate_response(prompt):

    # Primary model
    models = [
        "gemini-3.5-flash",
        "gemini-3.5-flash-lite"
    ]

    for model_name in models:

        try:

            print(
                f"\n[Order Agent] Using model: {model_name}"
            )

            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            if response and response.text:

                return response.text

        except Exception as error:

            print(
                f"[Order Agent] {model_name} failed."
            )

            print(
                f"[Order Agent] Error: {error}"
            )

            # Try next model
            time.sleep(1)

    return (
        "I am currently unable to generate a response "
        "because the AI service is temporarily unavailable. "
        "Please try again shortly."
    )


# ============================================================
# ORDER AGENT
# ============================================================

def order_agent(user_message):

    order_id = extract_order_id(
        user_message
    )

    if not order_id:

        return (
            "Please provide your order ID so I can "
            "check your order status."
        )

    # --------------------------------------------------------
    # CALL ORDER TOOL
    # --------------------------------------------------------

    order_information = get_order_status(
        order_id
    )

    # --------------------------------------------------------
    # CREATE PROMPT
    # --------------------------------------------------------

    prompt = f"""
{ORDER_AGENT_PROMPT}

Customer request:
{user_message}

Order ID:
{order_id}

Information returned by the Order Tool:
{order_information}

Based only on the information above, provide a helpful
response to the customer.
"""

    # --------------------------------------------------------
    # GENERATE RESPONSE
    # --------------------------------------------------------

    return generate_response(
        prompt
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    user_message = input(
        "Enter your order request: "
    )

    result = order_agent(
        user_message
    )

    print("\n")
    print("=" * 60)
    print("ORDER AGENT RESPONSE")
    print("=" * 60)
    print(result)