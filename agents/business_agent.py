import os
import google.generativeai as genai

from tools.business_tools import (
    get_support_analytics,
    calculate_kpis,
    generate_business_report
)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3.6-flash")


BUSINESS_AGENT_PROMPT = """
You are a Business Decision Support Agent.

Your responsibility is to analyze customer-support information
and provide useful business insights.

You can analyze:
- Support tickets
- Customer issues
- KPIs
- Workload
- Support trends

Present information clearly for managers.
Do not make employment decisions about individual employees.
"""


def business_agent(user_message):

    data = generate_business_report()

    prompt = f"""
    {BUSINESS_AGENT_PROMPT}

    Manager's question:
    {user_message}

    Business data:
    {data}

    Analyze the information and provide a concise business insight.
    """

    response = model.generate_content(prompt)

    return response.text