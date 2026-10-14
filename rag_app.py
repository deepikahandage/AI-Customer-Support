
import streamlit as st
from pathlib import Path
from rag_chatbot import ask_rag_chatbot

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="SupportAI | AI Support Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge_base"

# ==========================================
# SESSION STATE
# ==========================================

defaults = {
    "rag_messages": [],
    "pending_question": None,
    "page": "Dashboard",
    "total_questions": 0,
    "answered_questions": 0,
    "failed_questions": 0,
    "activity": [],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = (
            value.copy() if isinstance(value, list) else value
        )

# ==========================================
# WEBSITE STYLING
# ==========================================

st.markdown("""
<style>
.stApp {
    background: #F4F7FC;
}

[data-testid="stSidebar"] {
    background: #101B3D;
}

[data-testid="stSidebar"] * {
    color: #F8FAFC;
}

.brand {
    font-size: 28px;
    font-weight: 800;
    color: white;
}

.brand-subtitle {
    font-size: 13px;
    color: #A9B8D8;
    margin-bottom: 25px;
}

.hero {
    background: linear-gradient(120deg, #14244F, #315DEB);
    padding: 30px;
    border-radius: 18px;
    color: white;
    margin-bottom: 24px;
}

.hero h1 {
    color: white;
    font-size: 32px;
    margin-bottom: 8px;
}

.hero p {
    color: #E0E9FF;
    font-size: 15px;
}

.section-title {
    color: #14244F;
    font-size: 23px;
    font-weight: 750;
    margin: 12px 0 18px 0;
}

.metric-card {
    background: white;
    border: 1px solid #E0E7F1;
    border-radius: 15px;
    padding: 20px;
    min-height: 125px;
    box-shadow: 0 3px 12px rgba(20, 36, 79, 0.04);
}

.metric-label {
    color: #64748B;
    font-size: 14px;
}

.metric-value {
    color: #14244F;
    font-size: 30px;
    font-weight: 800;
    margin-top: 8px;
}

.metric-icon {
    font-size: 23px;
}

.topic-card {
    background: white;
    border: 1px solid #E0E7F1;
    border-radius: 14px;
    padding: 18px;
    min-height: 115px;
    margin-bottom: 8px;
}

.topic-card h4 {
    color: #14244F;
    font-size: 17px;
}

.topic-card p {
    color: #64748B;
    font-size: 13px;
}

[data-testid="stChatMessage"] {
    background: white;
    border: 1px solid #E0E7F1;
    border-radius: 14px;
    padding: 12px;
    margin-bottom: 10px;
}

div.stButton > button {
    border-radius: 10px;
    min-height: 42px;
    font-weight: 600;
}

.footer {
    text-align: center;
    color: #64748B;
    font-size: 12px;
    padding: 24px 0;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def get_knowledge_files():
    if not KNOWLEDGE_DIR.exists():
        return []

    return sorted(
        file for file in KNOWLEDGE_DIR.iterdir()
        if file.is_file()
    )


def show_metric(icon, label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def get_success_rate():
    total = st.session_state.total_questions

    if total == 0:
        return 0

    return round(
        st.session_state.answered_questions / total * 100
    )


def record_question(question, answer):
    answer = str(answer).strip()

    error_prefixes = (
        "The AI service",
        "The configured Gemini model",
        "The chatbot could not",
        "The Gemini API",
        "Gemini returned an empty",
        "The AI service credentials",
    )

    failed = not answer or answer.startswith(error_prefixes)

    st.session_state.total_questions += 1

    if failed:
        st.session_state.failed_questions += 1
        status = "Needs attention"
    else:
        st.session_state.answered_questions += 1
        status = "Answered"

    st.session_state.activity.insert(0, {
        "question": question,
        "status": status
    })

    st.session_state.activity = st.session_state.activity[:10]


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

with st.sidebar:
    st.markdown(
        '<div class="brand">🤖 SupportAI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="brand-subtitle">'
        'AI Customer Support Platform</div>',
        unsafe_allow_html=True
    )

    st.divider()
    st.caption("WORKSPACE")

    if st.button("📊 Dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"
        st.rerun()

    if st.button("💬 RAG Chatbot", use_container_width=True):
        st.session_state.page = "RAG Chatbot"
        st.rerun()

    if st.button("📚 Knowledge Base", use_container_width=True):
        st.session_state.page = "Knowledge Base"
        st.rerun()

    st.divider()

    st.markdown("### Support Categories")
    st.markdown("📦 Order information")
    st.markdown("💰 Refund assistance")
    st.markdown("🔄 Returns")
    st.markdown("🛠️ Technical support")
    st.markdown("🛍️ Product information")

    st.divider()
    st.caption("RAG · Python · Streamlit · Gemini · ChromaDB")

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.rag_messages = []
        st.session_state.pending_question = None
        st.rerun()


# ==========================================
# DASHBOARD PAGE
# ==========================================

if st.session_state.page == "Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>SupportAI Dashboard</h1>
        <p>
            Welcome to your AI customer-support workspace.
            Monitor chatbot activity, review responses,
            and manage your support knowledge base.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Overview</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        show_metric(
            "💬", "Total Questions",
            st.session_state.total_questions
        )

    with c2:
        show_metric(
            "✅", "Answered",
            st.session_state.answered_questions
        )

    with c3:
        show_metric(
            "⚠️", "Needs Attention",
            st.session_state.failed_questions
        )

    with c4:
        show_metric(
            "📈", "Success Rate",
            f"{get_success_rate()}%"
        )

    st.markdown(
        '<div class="section-title">Support Workspace</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="topic-card">
            <h4>💬 RAG Customer Chatbot</h4>
            <p>
                Ask customer-support questions and retrieve
                answers from your knowledge-base documents.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Chatbot →", use_container_width=True):
            st.session_state.page = "RAG Chatbot"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="topic-card">
            <h4>📚 Knowledge Base</h4>
            <p>
                Review support documents and test whether
                the retrieval system can access their content.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("View Knowledge Base →", use_container_width=True):
            st.session_state.page = "Knowledge Base"
            st.rerun()

    st.markdown(
        '<div class="section-title">Recent Activity</div>',
        unsafe_allow_html=True
    )

    if st.session_state.activity:
        for item in st.session_state.activity[:5]:
            with st.container(border=True):
                st.write(f"**Question:** {item['question']}")
                st.caption(f"Status: {item['status']}")
    else:
        st.info(
            "No questions yet. Open the RAG Chatbot to start "
            "a conversation. Recent activity will appear here."
        )

    st.caption(
        "Statistics reflect activity in the current Streamlit "
        "session; they are not permanent historical analytics."
    )


# ==========================================
# RAG CHATBOT PAGE
# ==========================================

elif st.session_state.page == "RAG Chatbot":

    st.markdown("""
    <div class="hero">
        <h1>Customer Support Assistant</h1>
        <p>
            Ask about orders, returns, refunds, products,
            or technical issues. SupportAI searches the
            knowledge base to help you.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Explore Support Topics</div>',
        unsafe_allow_html=True
    )

    topics = [
        (
            "📦 Order Support",
            "Order status and delivery information.",
            "How can I check my order status?"
        ),
        (
            "💰 Refunds",
            "Understand the refund process.",
            "How can I request a refund?"
        ),
        (
            "🛠️ Technical Help",
            "Get help with product problems.",
            "My product is not working. What should I do?"
        ),
        (
            "🔄 Returns",
            "Help with damaged products.",
            "What should I do if my product arrives damaged?"
        )
    ]

    columns = st.columns(4)

    for index, (title, description, question_text) in enumerate(topics):
        with columns[index]:
            st.markdown(
                f"""
                <div class="topic-card">
                    <h4>{title}</h4>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "Ask",
                key=f"topic_{index}",
                use_container_width=True
            ):
                st.session_state.pending_question = question_text
                st.rerun()

    st.markdown(
        '<div class="section-title">💬 Chat with SupportAI</div>',
        unsafe_allow_html=True
    )

    for message in st.session_state.rag_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    typed_question = st.chat_input("Type your question here...")

    question = (
        typed_question
        or st.session_state.pending_question
    )

    if question:
        st.session_state.pending_question = None

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching the knowledge base..."):
                answer = ask_rag_chatbot(question)

            answer = str(answer).strip()
            st.markdown(answer)

        st.session_state.rag_messages.extend([
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer}
        ])

        record_question(question, answer)


# ==========================================
# KNOWLEDGE BASE PAGE
# ==========================================

elif st.session_state.page == "Knowledge Base":

    st.markdown("""
    <div class="hero">
        <h1>Knowledge Base</h1>
        <p>
            Review support documents and test whether
            ChromaDB can retrieve relevant content.
        </p>
    </div>
    """, unsafe_allow_html=True)

    files = get_knowledge_files()

    st.markdown(
        '<div class="section-title">Document Status</div>',
        unsafe_allow_html=True
    )

    if files:
        st.metric("Files Found", len(files))

        for file_path in files:
            with st.container(border=True):
                st.markdown(f"### 📄 {file_path.name}")

                if file_path.suffix.lower() != ".txt":
                    st.warning(
                        "This file exists, but the current "
                        "RAG loader reads TXT files only."
                    )
                    continue

                try:
                    content = file_path.read_text(
                        encoding="utf-8"
                    ).strip()

                    if content:
                        st.success("Document readable")
                        st.caption(
                            f"Characters: {len(content):,}"
                        )
                    else:
                        st.error("Document is empty")

                except Exception as error:
                    st.error("Could not read this document.")
                    st.code(
                        f"{type(error).__name__}: {error}"
                    )

        st.divider()

        st.markdown(
            '<div class="section-title">RAG Retrieval Test</div>',
            unsafe_allow_html=True
        )

        test_question = st.text_input(
            "Enter a test question",
            value="What should I do if my product arrives damaged?",
            key="kb_test_question"
        )

        if st.button(
            "Test Knowledge Retrieval",
            use_container_width=True
        ):
            if not test_question.strip():
                st.warning("Please enter a test question.")
            else:
                try:
                    from rag_chatbot import create_rag_system

                    with st.spinner("Testing ChromaDB retrieval..."):
                        vector_store, _ = create_rag_system()

                        results = vector_store.similarity_search(
                            test_question.strip(),
                            k=3
                        )

                    if results:
                        st.success(
                            f"Retrieval successful: "
                            f"{len(results)} chunk(s) returned."
                        )

                        for index, document in enumerate(
                            results, start=1
                        ):
                            with st.expander(
                                f"Retrieved result {index}"
                            ):
                                st.write(document.page_content)

                                source = document.metadata.get(
                                    "source", "Unknown source"
                                )
                                st.caption(f"Source: {source}")
                    else:
                        st.error(
                            "No relevant chunks were retrieved."
                        )

                except Exception as error:
                    st.error("Knowledge retrieval test failed.")
                    st.code(
                        f"{type(error).__name__}: {error}"
                    )

    else:
        st.error(
            "No documents found. Add a TXT file to the "
            "knowledge_base folder."
        )

    st.info(
        "Document readability and vector retrieval are different "
        "checks. Use the retrieval test to check ChromaDB."
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown("""
<div class="footer">
    SupportAI · AI-Powered Customer Support Dashboard<br>
    Built with Python, Streamlit, Gemini and Retrieval-Augmented Generation
</div>
""", unsafe_allow_html=True)
