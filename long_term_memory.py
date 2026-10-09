import json
import os


class LongTermMemory:

    def __init__(self, file_path="memory/long_term_memory.json"):

        self.file_path = file_path

        # Create memory file if it does not exist
        if not os.path.exists(self.file_path):

            with open(
                self.file_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump({}, file, indent=4)


    # ========================================================
    # LOAD MEMORY
    # ========================================================

    def load_memory(self):

        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):

            return {}


    # ========================================================
    # SAVE MEMORY
    # ========================================================

    def save_memory(self, memory):

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                memory,
                file,
                indent=4
            )


    # ========================================================
    # STORE CUSTOMER INFORMATION
    # ========================================================

    def store_customer(self, customer_id, information):

        memory = self.load_memory()

        if customer_id not in memory:

            memory[customer_id] = []

        memory[customer_id].append(information)

        self.save_memory(memory)


    # ========================================================
    # GET CUSTOMER INFORMATION
    # ========================================================

    def get_customer(self, customer_id):

        memory = self.load_memory()

        return memory.get(
            customer_id,
            []
        )


    # ========================================================
    # CLEAR CUSTOMER MEMORY
    # ========================================================

    def clear_customer(self, customer_id):

        memory = self.load_memory()

        if customer_id in memory:

            del memory[customer_id]

            self.save_memory(memory)


    # ========================================================
    # DISPLAY ALL MEMORY
    # ========================================================

    def display_all(self):

        memory = self.load_memory()

        print("\n")
        print("=" * 60)
        print("LONG-TERM MEMORY")
        print("=" * 60)

        if not memory:

            print("No long-term information stored.")

        else:

            for customer_id, information in memory.items():

                print(f"\nCustomer ID: {customer_id}")

                for item in information:

                    print(f"- {item}")


# ============================================================
# TEST LONG-TERM MEMORY
# ============================================================

if __name__ == "__main__":

    memory = LongTermMemory()

    memory.store_customer(
        "customer_1001",
        "Customer previously requested a refund for order 1001."
    )

    memory.store_customer(
        "customer_1001",
        "Customer reported that the product arrived damaged."
    )

    print("\nStored Customer Information:")

    information = memory.get_customer(
        "customer_1001"
    )

    for item in information:

        print("-", item)

    memory.display_all()