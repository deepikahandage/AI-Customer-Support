import os
import google.generativeai as genai

from tools.product_tools import search_products

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3.6-flash")


PRODUCT_AGENT_PROMPT = """
You are a Product Recommendation Agent.

Your responsibility is to recommend products based on:
- Customer requirements
- Budget
- Intended use

Do not invent product information.
Use the product search tool.
"""


def product_agent(user_message):

    products = search_products(category="Laptop")

    prompt = f"""
    {PRODUCT_AGENT_PROMPT}

    Customer request:
    {user_message}

    Available products:
    {products}

    Recommend appropriate products and explain why.
    """

    response = model.generate_content(prompt)

    return response.text