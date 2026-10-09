import streamlit as st
import json
import os
from datetime import datetime

from workflow import run_customer_workflow


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Customer Support Dashboard",
    page_icon="🤖",
    layout="wide"
)


# ==================================================
# LOAD WORKFLOW LOGS
# ==================================================

LOG_FILE = "workflow_logs.json"


def load_logs():

    if not os.path.exists(LOG_FILE):
        return []

    try:
        with open(
            LOG_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (json.JSONDecodeError, OSError):

        return []


# ==================================================
# TITLE
# ==================================================

st.title("🤖 AI Customer Support Dashboard")

st.write(
    "Multi-Agent Coordination and Decision Support System"
)


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("System Information")

st.sidebar.success("API Status: Active")

st.sidebar.write("### System Components")

st.sidebar.write("🤖 Specialized Agents: 5")
st.sidebar.write("🔧 Tool Groups: 5")
st.sidebar.write("🧠 Memory Systems: 3")
st.sidebar.write("🔄 Workflow Automation: Active")


# ==================================================
# LOAD LOGS
# ==================================================

logs = load_logs()

total_requests = len(logs)

completed_requests = sum(
    1
    for log in logs
    if log.get("status") == "Completed"
)

failed_requests = sum(
    1
    for log in logs
    if log.get("status") == "Failed"
)


# ==================================================
# TOP METRICS
# ==================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Requests",
        total_requests
    )

with col2:
    st.metric(
        "Completed",
        completed_requests
    )

with col3:
    st.metric(
        "Failed",
        failed_requests
    )

with col4:
    st.metric(
        "Specialized Agents",
        5
    )


st.divider()


# ==================================================
# AGENT STATUS
# ==================================================

st.subheader("🤖 Agent Status")

agent_col1, agent_col2, agent_col3 = st.columns(3)

with agent_col1:
    st.success("🟢 Supervisor Agent")
    st.caption(
        "Coordinates specialized agents."
    )

with agent_col2:
    st.success("🟢 Order Agent")
    st.caption(
        "Handles order and delivery queries."
    )

with agent_col3:
    st.success("🟢 Refund & Return Agent")
    st.caption(
        "Handles refund and return requests."
    )


agent_col4, agent_col5, agent_col6 = st.columns(3)

with agent_col4:
    st.success("🟢 Technical Support Agent")
    st.caption(
        "Handles technical problems."
    )

with agent_col5:
    st.success("🟢 Product Agent")
    st.caption(
        "Handles product recommendations."
    )

with agent_col6:
    st.success("🟢 Business Agent")
    st.caption(
        "Handles business and analytics queries."
    )


st.divider()


# ==================================================
# CUSTOMER REQUEST
# ==================================================

st.subheader("💬 Customer Request")

customer_message = st.text_area(
    "Enter your customer request:",
    placeholder=(
        "Example: My order 1001 arrived damaged "
        "and I want a refund."
    ),
    height=120
)


if st.button(
    "🚀 Process Customer Request",
    type="primary"
):

    if customer_message.strip():

        with st.spinner(
            "AI agents are processing the request..."
        ):

            try:

                response = run_customer_workflow(
                    customer_message
                )

                st.session_state["last_request"] = (
                    customer_message
                )

                st.session_state["last_response"] = (
                    response
                )

                st.session_state["last_time"] = (
                    datetime.now().strftime(
                        "%d-%m-%Y %H:%M:%S"
                    )
                )

                st.success(
                    "Workflow completed successfully!"
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"Workflow Error: {e}"
                )

    else:

        st.warning(
            "Please enter a customer request."
        )


# ==================================================
# WORKFLOW PIPELINE
# ==================================================

st.divider()

st.subheader("🔄 Workflow Pipeline")

workflow_col1, workflow_col2 = st.columns(2)

with workflow_col1:

    st.write("### Processing Flow")

    st.write("1️⃣ Customer Request")
    st.write("⬇")
    st.write("2️⃣ Supervisor Agent")
    st.write("⬇")
    st.write("3️⃣ Specialized Agent(s)")
    st.write("⬇")
    st.write("4️⃣ Tools")
    st.write("⬇")
    st.write("5️⃣ Shared Memory")
    st.write("⬇")
    st.write("6️⃣ Final Response")


with workflow_col2:

    st.write("### Memory Systems")

    st.success(
        "🧠 Shared Memory — Agent communication"
    )

    st.info(
        "💬 Short-Term Memory — Current conversation"
    )

    st.warning(
        "🗄️ Long-Term Memory — Persistent customer information"
    )


# ==================================================
# LATEST RESPONSE
# ==================================================

if "last_response" in st.session_state:

    st.divider()

    st.subheader("💡 Latest AI Response")

    st.write(
        st.session_state["last_response"]
    )


# ==================================================
# WORKFLOW HISTORY
# ==================================================

st.divider()

st.subheader("📊 Workflow History")

logs = load_logs()

if logs:

    # Show latest 10 workflow records
    recent_logs = list(
        reversed(logs[-10:])
    )

    for log in recent_logs:

        status = log.get(
            "status",
            "Unknown"
        )

        if status == "Completed":

            st.success(
                f"✅ {status}"
            )

        else:

            st.error(
                f"❌ {status}"
            )

        st.write(
            f"**Time:** "
            f"{log.get('timestamp', '-')}"
        )

        st.write(
            f"**Execution Time:** "
            f"{log.get('duration_seconds', 0)} seconds"
        )

        st.write(
            f"**Customer Request:** "
            f"{log.get('customer_message', '-')}"
        )

        st.write(
            f"**Response:** "
            f"{log.get('response', '-')}"
        )

        if log.get("error"):

            st.error(
                f"Error: {log.get('error')}"
            )

        st.divider()

else:

    st.info(
        "No workflow activity recorded yet."
    )


# ==================================================
# PERFORMANCE SUMMARY
# ==================================================

st.subheader("⏱️ Performance Summary")

completed_logs = [
    log
    for log in logs
    if log.get("status") == "Completed"
    and isinstance(
        log.get("duration_seconds"),
        (int, float)
    )
]

if completed_logs:

    total_time = sum(
        log["duration_seconds"]
        for log in completed_logs
    )

    average_time = (
        total_time / len(completed_logs)
    )

    fastest_time = min(
        log["duration_seconds"]
        for log in completed_logs
    )

    slowest_time = max(
        log["duration_seconds"]
        for log in completed_logs
    )

    performance_col1, performance_col2, performance_col3 = (
        st.columns(3)
    )

    with performance_col1:

        st.metric(
            "Average Response Time",
            f"{average_time:.2f} sec"
        )

    with performance_col2:

        st.metric(
            "Fastest Workflow",
            f"{fastest_time:.2f} sec"
        )

    with performance_col3:

        st.metric(
            "Slowest Workflow",
            f"{slowest_time:.2f} sec"
        )

else:

    st.info(
        "Performance data will appear after workflow execution."
    )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "AI Customer Support | "
    "Multi-Agent Coordination & Decision Engine"
)