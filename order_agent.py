import os

from dotenv import load_dotenv
from google import genai

from tools.order_tools import get_order_status

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found. Check your .env file."
    )

client = genai.Client(api_key=api_key)


def order_agent(user_message):

    order_id = None

    for possible_id in ["1001", "1002", "1003"]:
        if possible_id in user_message:
            order_id = possible_id
            break

    if not order_id:
        return "Please provide your order ID."

    order_information = get_order_status(order_id)

    prompt = f"""
You are an Order Support Agent.

Your responsibility is to help customers with:
- Order status
- Delivery information
- Tracking information

Do not invent order information.

Customer question:
{user_message}

Order tool result:
{order_information}

Give a polite and clear response.
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text