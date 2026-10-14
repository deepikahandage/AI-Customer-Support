from rag_chatbot import ask_rag_chatbot

question = "What should a customer do if a product arrives damaged?"

print("\nCustomer Question:")
print(question)

print("\nRAG Chatbot Answer:")

try:
    answer = ask_rag_chatbot(question)
    print(answer)

except Exception as error:
    print("Error:", error)