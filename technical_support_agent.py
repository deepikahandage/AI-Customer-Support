import os
import google.generativeai as genai

from tools.technical_tools import (
    search_troubleshooting,
    check_warranty,
    create_support_ticket
)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3.6-flash")


TECHNICAL_AGENT_PROMPT = """
You are a Technical Support Agent.

Help customers troubleshoot technical problems.
You can use troubleshooting, warranty and support-ticket tools.

Give simple step-by-step solutions.
"""


def technical_agent(user_message):

    result = search_troubleshooting(user_message)

    prompt = f"""
    {TECHNICAL_AGENT_PROMPT}

    Customer problem:
    {user_message}

    Tool result:
    {result}

    Give a clear response.
    """

    response = model.generate_content(prompt)

    return response.text