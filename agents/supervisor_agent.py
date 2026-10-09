from agents.order_agent import order_agent
from agents.refund_agent import refund_agent
from agents.technical_support_agent import technical_agent
from agents.product_agent import product_agent
from agents.business_agent import business_agent
from agents.customer_support_agent import customer_support_agent

from memory.shared_memory import SharedMemory
from memory.short_term_memory import ShortTermMemory
from memory.long_term_memory import LongTermMemory


# ============================================================
# MEMORY SYSTEMS
# ============================================================

shared_memory = SharedMemory()
short_term_memory = ShortTermMemory()
long_term_memory = LongTermMemory()


# ============================================================
# SUPERVISOR AGENT
# ============================================================

def supervisor_agent(user_message):

    # --------------------------------------------------------
    # STORE CUSTOMER REQUEST IN SHORT-TERM MEMORY
    # --------------------------------------------------------

    short_term_memory.add_message(
        "Customer",
        user_message
    )

    # --------------------------------------------------------
    # STORE CUSTOMER REQUEST IN LONG-TERM MEMORY
    # --------------------------------------------------------

    long_term_memory.store_customer(
        "customer_1001",
        user_message
    )

    message = user_message.lower()

    results = []


    # ========================================================
    # ORDER AGENT
    # ========================================================

    if any(word in message for word in [
        "order",
        "tracking",
        "delivery",
        "shipped",
        "delivered"
    ]):

        print("\n[Supervisor] Calling Order Agent...")

        order_result = order_agent(user_message)

        # Store in Shared Memory
        shared_memory.store(
            "order_agent_result",
            order_result
        )

        # Store in Short-Term Memory
        short_term_memory.add_message(
            "Order Agent",
            order_result
        )

        # Store important result in Long-Term Memory
        long_term_memory.store_customer(
            "customer_1001",
            "Order Agent: " + order_result
        )

        results.append(
            "Order Agent:\n" + order_result
        )


    # ========================================================
    # REFUND & RETURN AGENT
    # ========================================================

    if any(word in message for word in [
        "refund",
        "return",
        "money back",
        "exchange"
    ]):

        print("\n[Supervisor] Calling Refund & Return Agent...")

        refund_result = refund_agent(
            user_message,
            shared_memory
        )

        # Store in Shared Memory
        shared_memory.store(
            "refund_agent_result",
            refund_result
        )

        # Store in Short-Term Memory
        short_term_memory.add_message(
            "Refund Agent",
            refund_result
        )

        # Store important result in Long-Term Memory
        long_term_memory.store_customer(
            "customer_1001",
            "Refund Agent: " + refund_result
        )

        results.append(
            "Refund & Return Agent:\n" + refund_result
        )


    # ========================================================
    # TECHNICAL SUPPORT AGENT
    # ========================================================

    if any(word in message for word in [
        "technical",
        "not working",
        "error",
        "wifi",
        "internet",
        "slow"
    ]):

        print("\n[Supervisor] Calling Technical Support Agent...")

        technical_result = technical_agent(user_message)

        shared_memory.store(
            "technical_agent_result",
            technical_result
        )

        short_term_memory.add_message(
            "Technical Support Agent",
            technical_result
        )

        long_term_memory.store_customer(
            "customer_1001",
            "Technical Support Agent: " + technical_result
        )

        results.append(
            "Technical Support Agent:\n" + technical_result
        )


    # ========================================================
    # PRODUCT RECOMMENDATION AGENT
    # ========================================================

    if any(word in message for word in [
        "recommend",
        "recommendation",
        "suggest",
        "laptop",
        "product",
        "buy"
    ]):

        print("\n[Supervisor] Calling Product Recommendation Agent...")

        product_result = product_agent(user_message)

        shared_memory.store(
            "product_agent_result",
            product_result
        )

        short_term_memory.add_message(
            "Product Recommendation Agent",
            product_result
        )

        long_term_memory.store_customer(
            "customer_1001",
            "Product Agent: " + product_result
        )

        results.append(
            "Product Recommendation Agent:\n" + product_result
        )


    # ========================================================
    # BUSINESS DECISION SUPPORT AGENT
    # ========================================================

    if any(word in message for word in [
        "business",
        "analytics",
        "kpi",
        "report",
        "workload",
        "tickets",
        "manager"
    ]):

        print("\n[Supervisor] Calling Business Decision Support Agent...")

        business_result = business_agent(user_message)

        shared_memory.store(
            "business_agent_result",
            business_result
        )

        short_term_memory.add_message(
            "Business Decision Support Agent",
            business_result
        )

        long_term_memory.store_customer(
            "customer_1001",
            "Business Agent: " + business_result
        )

        results.append(
            "Business Decision Support Agent:\n" + business_result
        )


    # ========================================================
    # GENERAL CUSTOMER SUPPORT AGENT
    # ========================================================

    if not results:

        print("\n[Supervisor] Calling Customer Support Agent...")

        support_result = customer_support_agent(
            user_message
        )

        shared_memory.store(
            "customer_support_result",
            support_result
        )

        short_term_memory.add_message(
            "Customer Support Agent",
            support_result
        )

        long_term_memory.store_customer(
            "customer_1001",
            "Customer Support Agent: " + support_result
        )

        results.append(
            "Customer Support Agent:\n" + support_result
        )


    # ========================================================
    # COMBINE AGENT RESULTS
    # ========================================================

    final_response = "\n\n".join(results)

    return final_response


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("       AI CUSTOMER SUPPORT")
    print("       MULTI-AGENT COORDINATION SYSTEM")
    print("=" * 60)

    # --------------------------------------------------------
    # GET USER INPUT
    # --------------------------------------------------------

    user_message = input(
        "\nEnter your customer request: "
    )

    print("\nProcessing request...")


    # --------------------------------------------------------
    # RUN SUPERVISOR
    # --------------------------------------------------------

    response = supervisor_agent(
        user_message
    )


    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    print("\n")
    print("=" * 60)
    print("FINAL RESPONSE")
    print("=" * 60)

    print(response)


    # ========================================================
    # SHARED MEMORY
    # ========================================================

    print("\n")
    print("=" * 60)
    print("SHARED MEMORY")
    print("=" * 60)

    memory_data = shared_memory.get_all()

    if memory_data:

        for key, value in memory_data.items():

            print(f"\n{key}:")
            print(value)

    else:

        print("No information stored.")


    # ========================================================
    # SHORT-TERM MEMORY
    # ========================================================

    print("\n")
    print("=" * 60)
    print("SHORT-TERM CONVERSATION MEMORY")
    print("=" * 60)

    print(
        short_term_memory.get_context()
    )


    # ========================================================
    # LONG-TERM MEMORY
    # ========================================================

    print("\n")
    print("=" * 60)
    print("LONG-TERM MEMORY")
    print("=" * 60)

    customer_history = long_term_memory.get_customer(
        "customer_1001"
    )

    if customer_history:

        for item in customer_history:

            print("-", item)

    else:

        print("No long-term information found.")


    # ========================================================
    # COMPLETION
    # ========================================================

    print("\n")
    print("=" * 60)
    print("MULTI-AGENT WORKFLOW COMPLETED")
    print("=" * 60)