import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3.6-flash")


CUSTOMER_SUPPORT_PROMPT = """
You are a General Customer Support Agent.

Handle general customer questions.

If the question is specifically about:
- Orders → Order Agent
- Refunds or returns → Refund Agent
- Technical problems → Technical Support Agent
- Product recommendations → Product Agent
- Business analytics → Business Decision Support Agent

For general questions, answer politely.
"""


def customer_support_agent(user_message):

    prompt = f"""
    {CUSTOMER_SUPPORT_PROMPT}

    Customer:
    {user_message}

    Give a helpful response.
    """

    response = model.generate_content(prompt)

    return response.text