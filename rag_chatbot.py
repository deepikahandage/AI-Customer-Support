
import os
from pathlib import Path
from functools import lru_cache

from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI,
)
from langchain_chroma import Chroma


# --------------------------------------------------
# 1. Project paths and configuration
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge_base"
DB_DIR = BASE_DIR / "chroma_db"

load_dotenv(BASE_DIR / ".env")


def get_api_key():
    """Read the Gemini API key from the .env file."""
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. "
            "Check your project's .env file."
        )

    return api_key


# --------------------------------------------------
# 2. Load customer-support documents
# --------------------------------------------------

def load_knowledge_documents():
    """Load all TXT documents from the knowledge_base folder."""
    if not KNOWLEDGE_DIR.exists():
        raise FileNotFoundError(
            f"Knowledge-base folder not found: {KNOWLEDGE_DIR}"
        )

    documents = []

    for file_path in KNOWLEDGE_DIR.glob("*.txt"):
        documents.extend(
            TextLoader(
                str(file_path),
                encoding="utf-8"
            ).load()
        )

    if not documents:
        raise ValueError(
            "No .txt documents found in knowledge_base."
        )

    print(f"Loaded {len(documents)} source document(s).")

    return documents


# --------------------------------------------------
# 3. Create the RAG system
# --------------------------------------------------

@lru_cache(maxsize=1)
def create_rag_system():
    """Create embeddings, vector database, and Gemini model."""
    api_key = get_api_key()

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key,
        max_retries=2,
    )

    # Reuse the existing local vector database if available.
    if DB_DIR.exists() and any(DB_DIR.iterdir()):
        print("Loading existing Chroma vector database...")

        vector_store = Chroma(
            persist_directory=str(DB_DIR),
            embedding_function=embeddings,
        )

    else:
        print("Creating Chroma vector database...")

        documents = load_knowledge_documents()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=80,
        )

        chunks = splitter.split_documents(documents)

        if not chunks:
            raise ValueError(
                "No text chunks were created from the documents."
            )

        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=str(DB_DIR),
        )

        print(f"Stored {len(chunks)} text chunk(s).")

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=api_key,
        max_retries=2,
        timeout=60,
    )

    return vector_store, llm


# --------------------------------------------------
# 4. Convert errors into helpful messages
# --------------------------------------------------

def friendly_error(error):
    """Return a readable error without exposing credentials."""
    message = str(error).lower()

    if "429" in message or "quota" in message or "rate limit" in message:
        return (
            "The AI service request limit has been reached. "
            "Please wait before trying again."
        )

    if "503" in message or "unavailable" in message:
        return (
            "The AI service is temporarily busy. "
            "Please try again shortly."
        )

    if "404" in message or "not_found" in message:
        return (
            "The configured Gemini model is unavailable. "
            "Check the model supported by your API account."
        )

    if (
        "api key" in message
        or "api_key" in message
        or "credentials" in message
        or "permission_denied" in message
        or "401" in message
        or "403" in message
    ):
        return (
            "The Gemini API credentials could not be verified. "
            "Check your local .env configuration and API access."
        )

    if "timeout" in message or "timed out" in message:
        return (
            "The AI service took too long to respond. "
            "Please try again."
        )

    return (
        "The chatbot could not complete your request. "
        "Please check the terminal for the error details."
    )


# --------------------------------------------------
# 5. Ask a question using Retrieval-Augmented Generation
# --------------------------------------------------

def ask_rag_chatbot(question):
    """Retrieve relevant support documents and generate an answer."""

    if not question or not question.strip():
        return "Please enter a question."

    try:
        vector_store, llm = create_rag_system()

        clean_question = question.strip()

        print(f"\nCustomer question: {clean_question}")

        # Retrieve relevant knowledge-base content.
        relevant_docs = vector_store.similarity_search(
            clean_question,
            k=3,
        )

        if not relevant_docs:
            return (
                "I couldn't find relevant information in the "
                "customer-support knowledge base."
            )

        context = "\n\n".join(
            document.page_content
            for document in relevant_docs
        )

        prompt = f"""
You are SupportAI, a polite customer-support assistant.

Rules:
1. Answer using the provided knowledge-base context.
2. Do not invent order statuses, tracking numbers, or policies.
3. Do not claim that a refund or return has been approved.
4. If the context does not contain the answer, explain that
   the information is unavailable and suggest contacting support.
5. Give a clear, helpful answer in simple English.
6. Use numbered steps when explaining troubleshooting.

KNOWLEDGE-BASE CONTEXT:
{context}

CUSTOMER QUESTION:
{clean_question}

ANSWER:
"""

        # Generate the answer.
        response = llm.invoke(prompt)

        answer = response.content

        # Debugging: inspect the response returned by Gemini.
        print("Gemini response content:", repr(answer))

        # Some model integrations may return content blocks.
        if isinstance(answer, list):
            text_parts = []

            for part in answer:
                if isinstance(part, str):
                    text_parts.append(part)

                elif isinstance(part, dict):
                    if part.get("type") == "text":
                        text_parts.append(part.get("text", ""))

            answer = "\n".join(text_parts)

        if isinstance(answer, str) and answer.strip():
            return answer.strip()

        print("Gemini returned an empty response.")

        return (
            "Gemini returned an empty response. "
            "Please try again and check the terminal."
        )

    except Exception as error:
        # Keep detailed diagnostic information in the terminal.
        print(
            f"RAG backend error: "
            f"{type(error).__name__}: {error}"
        )

        return friendly_error(error)


# --------------------------------------------------
# 6. Run the chatbot directly from the terminal
# --------------------------------------------------

if __name__ == "__main__":
    print("SupportAI RAG Chatbot")
    print("Type 'exit' to stop.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if question:
            print("\nSupportAI:")
            print(ask_rag_chatbot(question))
            print()
