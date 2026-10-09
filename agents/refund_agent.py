import os
import re

from dotenv import load_dotenv
from google import genai

from tools.refund_tools import (
    check_return_eligibility,
    check_refund_status,
    create_return_request
)


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found. Check your .env file."
    )

client = genai.Client(
    api_key=api_key
)


# ============================================================
# REFUND AGENT PROMPT
# ============================================================

REFUND_AGENT_PROMPT = """
You are a Refund and Return Agent in a multi-agent
AI customer support system.

Your responsibilities are:

1. Refund status
2. Return eligibility
3. Return requests
4. Refund-related customer support

Rules:

- Use information from the refund tools.
- Use information from Shared Memory when available.
- Never invent refund information.
- Do not claim that a refund was processed unless the tool
  confirms it.
- If the customer reports a damaged product, explain the
  appropriate next step.
- Be polite, clear and helpful.
"""


# ============================================================
# EXTRACT ORDER ID
# ============================================================

def extract_order_id(user_message):

    match = re.search(
        r"(?:order\s*|ord\s*)?(\d{4})",
        user_message,
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    return None


# ============================================================
# REFUND AGENT
# ============================================================

def refund_agent(
    user_message,
    shared_memory=None
):

    print(
        "\n[Refund Agent] Reading information from Shared Memory..."
    )

    # --------------------------------------------------------
    # GET ORDER ID
    # --------------------------------------------------------

    order_id = extract_order_id(
        user_message
    )

    if not order_id:

        return (
            "Please provide your order ID so I can "
            "check your refund or return request."
        )

    # --------------------------------------------------------
    # READ SHARED MEMORY
    # --------------------------------------------------------

    order_agent_information = ""

    if shared_memory is not None:

        try:

            order_agent_information = (
                shared_memory.get(
                    "order_agent_result"
                )
            )

        except Exception:

            order_agent_information = ""

    if order_agent_information:

        print(
            "\nInformation received from Order Agent:"
        )

        print(
            order_agent_information
        )

    # --------------------------------------------------------
    # CHECK REFUND STATUS
    # --------------------------------------------------------

    refund_status = check_refund_status(
        order_id
    )

    # --------------------------------------------------------
    # CHECK RETURN ELIGIBILITY
    # --------------------------------------------------------

    return_eligibility = check_return_eligibility(
        order_id
    )

    # --------------------------------------------------------
    # DAMAGED PRODUCT
    # --------------------------------------------------------

    message = user_message.lower()

    if "damaged" in message or "damage" in message:

        tool_result = (
            f"Refund Status: {refund_status}\n"
            f"Return Eligibility: {return_eligibility}"
        )

    elif "return" in message:

        tool_result = (
            f"Return Eligibility: {return_eligibility}\n"
            f"Refund Status: {refund_status}"
        )

    else:

        tool_result = (
            f"Refund Status: {refund_status}"
        )

    # --------------------------------------------------------
    # CREATE PROMPT
    # --------------------------------------------------------

    prompt = f"""
{REFUND_AGENT_PROMPT}

Customer request:
{user_message}

Order ID:
{order_id}

Information received from Order Agent:
{order_agent_information}

Refund and Return Tool Results:
{tool_result}

Respond to the customer.

If the refund has not been initiated, do not say that it
has been completed.

If the customer reports a damaged product, explain that
the return/refund process may require confirmation or
additional information.

Keep the response professional and easy to understand.
"""

    # --------------------------------------------------------
    # CALL GEMINI
    # --------------------------------------------------------

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        if response and response.text:

            return response.text

    except Exception as error:

        print(
            "\n[Refund Agent] Gemini error:"
        )

        print(error)

        return (
            "I checked the refund information, but the "
            "AI response service is temporarily unavailable. "
            "Please try again shortly."
        )

    return (
        "I could not generate a refund response right now."
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    user_message = input(
        "Enter your refund request: "
    )

    result = refund_agent(
        user_message
    )

    print("\n")
    print("=" * 60)
    print("REFUND AGENT RESPONSE")
    print("=" * 60)

    print(result)