# 🤖 AI Customer Support System

## 📌 Project Overview

AI Customer Support is a **multi-agent AI system** designed to provide intelligent and automated customer support.

The system uses multiple specialized AI agents. Each agent is responsible for a specific customer-support task and can use dedicated tools to complete that task.

The application is developed using **Python, Streamlit, and Google Gemini API**.

---

## 🎯 Project Objective

The main objective of this project is to develop a multi-agent customer-support system that can:

* Understand customer queries
* Route queries to the appropriate AI agent
* Handle order-related questions
* Handle refunds and returns
* Provide technical support
* Recommend products
* Provide business-support analytics
* Automate common customer-support tasks

---

## 🏗️ System Architecture

```text
                    Customer
                       │
                       ▼
              ┌─────────────────┐
              │ Supervisor Agent│
              └────────┬────────┘
                       │
       ┌───────────────┼────────────────┐
       │               │                │
       ▼               ▼                ▼
 Order Agent     Refund Agent     Technical Agent
       │               │                │
       ▼               ▼                ▼
 Order Tools      Refund Tools     Technical Tools

                       │
              ┌────────┴─────────┐
              ▼                  ▼
       Product Agent       Business Agent
              │                  │
              ▼                  ▼
       Product Tools       Business Tools
```

---

## 🤖 AI Agents

### 1. Supervisor Agent

The Supervisor Agent receives the customer's request and routes it to the appropriate specialized agent.

### 2. Customer Support Agent

Handles general customer-support questions and provides basic assistance.

### 3. Order Agent

Handles:

* Order status
* Order tracking
* Delivery information

### 4. Refund & Return Agent

Handles:

* Return eligibility
* Refund status
* Return requests

### 5. Technical Support Agent

Handles:

* Technical problems
* Basic troubleshooting
* Support requests

### 6. Product Recommendation Agent

Helps customers find suitable products based on their requirements.

### 7. Business Decision Support Agent

Analyzes customer-support information and provides business insights such as:

* Support ticket statistics
* Customer issue analysis
* KPIs
* Workload information
* Business reports

---

## 🛠️ Tools Used

The agents use specialized tools to perform specific operations.

### Order Tools

* `get_order_status()`
* `get_tracking_details()`
* `get_delivery_date()`

### Refund Tools

* `check_return_eligibility()`
* `check_refund_status()`
* `create_return_request()`

### Technical Support Tools

* `search_troubleshooting()`
* `check_warranty()`
* `create_support_ticket()`

### Product Tools

* `search_products()`
* `get_product_details()`
* `compare_products()`

### Business Tools

* `get_support_analytics()`
* `calculate_kpis()`
* `generate_business_report()`

---

## 💻 Technologies Used

* **Python**
* **Google Gemini API**
* **Google GenAI Python SDK**
* **Streamlit**
* **python-dotenv**
* **Git**
* **GitHub**

---

## 📂 Project Structure

```text
AI_Customer_Support/
│
├── agents/
│   ├── supervisor_agent.py
│   ├── customer_support_agent.py
│   ├── order_agent.py
│   ├── refund_agent.py
│   ├── technical_support_agent.py
│   ├── product_agent.py
│   └── business_agent.py
│
├── tools/
│   ├── order_tools.py
│   ├── refund_tools.py
│   ├── technical_tools.py
│   ├── product_tools.py
│   └── business_tools.py
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env.example
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the project folder

```bash
cd AI_Customer_Support
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

For Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 API Key Configuration

Create a `.env` file in the project root directory.

Add:

```text
GEMINI_API_KEY=YOUR_API_KEY
```

**Do not upload the `.env` file to GitHub.**

The API key is kept private using `.gitignore`.

---

## ▶️ How to Run

Run the following command:

```bash
streamlit run app.py
```

The application will open in your web browser.

---

## 🧪 Example Queries

### Order Agent

```text
Where is my order 1001?
```

### Refund & Return Agent

```text
Can I return order 1001?
```

### Technical Support Agent

```text
My laptop is not turning on.
```

### Product Recommendation Agent

```text
Recommend a laptop for programming.
```

### Business Decision Support Agent

```text
Give me a support analytics report.
```

---

## 🔄 Example Workflow

```text
Customer Query
      ↓
Supervisor Agent
      ↓
Identify Request
      ↓
Specialized Agent
      ↓
Relevant Tool
      ↓
Tool Result
      ↓
Gemini
      ↓
Customer Response
```

---

## 📊 Business Benefits

The system can help organizations by:

* Reducing repetitive customer-support work
* Providing faster responses
* Separating support responsibilities among specialized agents
* Analyzing customer-support information
* Providing business insights
* Improving support-team workflow
* Supporting data-driven operational decisions

---

## 🔒 Security

* API keys are stored in environment variables.
* `.env` is excluded from GitHub using `.gitignore`.
* Sensitive credentials should never be committed to the repository.

---

## 🚀 Future Enhancements

Future versions can include:

* Real customer/order database
* Real-time order tracking API
* Voice-based customer support
* Multilingual support
* Authentication and user accounts
* Advanced analytics dashboard
* Human-agent handoff
* Persistent conversation history
* More advanced agent-to-agent communication
* Production deployment

---

## 👩‍💻 Project

**Project:** AI Customer Support System
**Type:** Multi-Agent AI Application
**Technology:** Python, Google Gemini, Streamlit

Developed as part of an **Infosys Internship Project**.
