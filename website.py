import streamlit as st
import google.generativeai as genai

# -----------------------------
# API KEY
# -----------------------------
API_KEY = "PASTE_YOUR_NEW_GEMINI_KEY_HERE"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-3.6-flash")

# -----------------------------
# PAGE
# -----------------------------
st.set_page_config(
    page_title="AI Business Coordination Agent",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Business Coordination Agent")
st.write("One AI agent with multiple business support capabilities.")

# -----------------------------
# AGENTS / CAPABILITIES
# -----------------------------
st.subheader("Available AI Agents")

st.write("🛍️ Customer Support Agent")
st.write("💰 Refund & Return Agent")
st.write("📈 Business Decision Support Agent")
st.write("📦 Product Recommendation Agent")
st.write("🔧 Technical Support Agent")

st.divider()

# -----------------------------
# USER INPUT
# -----------------------------
user_input = st.text_input(
    "Ask your business-related question:"
)

if st.button("Ask AI Agent"):

    if user_input:

        prompt = f"""
You are an AI Business Coordination Agent.

You have five capabilities:

1. Customer Support Agent
   - Orders
   - Delivery
   - Complaints
   - Customer questions

2. Refund & Return Agent
   - Refunds
   - Returns
   - Order cancellation

3. Business Decision Support Agent
   - Sales
   - Marketing
   - Business strategy
   - Business decisions

4. Product Recommendation Agent
   - Product suggestions
   - Product comparison
   - Choosing products

5. Technical Support Agent
   - Technical problems
   - Website problems
   - Application problems

First identify which capability is required.

Then answer the user's question clearly and professionally.

User question:
{user_input}
"""

        with st.spinner("AI Agent is thinking..."):

            response = model.generate_content(prompt)

        st.subheader("🤖 AI Agent Response")
        st.write(response.text)

    else:
        st.warning("Please enter a question.")