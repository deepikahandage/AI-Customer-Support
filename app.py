import os
import streamlit as st
from dotenv import load_dotenv

from agents.supervisor_agent import supervisor_agent


load_dotenv()


st.set_page_config(
    page_title="AI Customer Support",
    page_icon="🤖",
    layout="centered"
)


st.title("🤖 AI Customer Support System")

st.write(
    "Multi-Agent Customer Support System using "
    "Google Gemini and specialized AI agents."
)


user_message = st.text_area(
    "Enter your question:",
    placeholder="Example: Where is my order 1001?"
)


if st.button("Submit"):

    if user_message.strip():

        with st.spinner("AI Agent is processing your request..."):

            response = supervisor_agent(user_message)

        st.subheader("AI Response")
        st.write(response)

    else:
        st.warning("Please enter a question.")