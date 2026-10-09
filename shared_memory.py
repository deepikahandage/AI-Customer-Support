class SharedMemory:
    def __init__(self):
        self.data = {}

    def store(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

    def get_all(self):
        return self.data

    def clear(self):
        self.data = {}


if __name__ == "__main__":

    memory = SharedMemory()

    # Order Agent stores information
    memory.store("order_id", "ORD1001")
    memory.store("order_status", "Delivered")
    memory.store("product", "Laptop")

    # Refund Agent retrieves information
    print("Information available to agents:")
    print(memory.get_all())

    print("\nOrder ID:")
    print(memory.get("order_id"))

    print("\nOrder Status:")
    print(memory.get("order_status"))