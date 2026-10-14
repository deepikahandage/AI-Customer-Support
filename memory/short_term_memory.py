class ShortTermMemory:
    def __init__(self):
        self.conversation = []

    def add_message(self, role, message):
        self.conversation.append({
            "role": role,
            "message": message
        })

    def get_messages(self):
        return self.conversation

    def get_context(self):
        context = ""

        for item in self.conversation:
            context += f"{item['role']}: {item['message']}\n"

        return context

    def clear(self):
        self.conversation = []


if __name__ == "__main__":

    memory = ShortTermMemory()

    memory.add_message("Customer", "My order number is ORD1001.")
    memory.add_message("Customer", "The product arrived damaged.")
    memory.add_message("Customer", "I want a refund.")

    print("Conversation Memory:")
    print(memory.get_context())