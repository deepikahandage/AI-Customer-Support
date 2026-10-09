from agents.supervisor_agent import supervisor_agent
from monitoring import log_workflow
import time


def run_customer_workflow(customer_message):
    """
    Main workflow for the AI Customer Support system.

    Customer Request
          ↓
    Supervisor Agent
          ↓
    Specialized Agent(s)
          ↓
    Tools + Memory
          ↓
    Final Response
          ↓
    Monitoring Log
    """

    print("\n========================================")
    print("      AI CUSTOMER SUPPORT WORKFLOW")
    print("========================================")

    print("\n[1] Customer Request:")
    print(customer_message)

    print("\n[2] Supervisor Agent:")
    print("Analyzing the request and selecting the required agent(s)...")

    start_time = time.time()

    try:

        response = supervisor_agent(customer_message)

        duration = time.time() - start_time

        log_workflow(
            customer_message,
            "Completed",
            response,
            "",
            duration
        )

        print("\n[3] Agent Processing Completed")

        print(
            f"\n[Performance] "
            f"Workflow completed in {duration:.2f} seconds"
        )

        print("\n[4] Final Customer Response:")
        print(response)

        print("\n========================================")
        print("       WORKFLOW COMPLETED")
        print("========================================")

        return response

    except Exception as e:

        duration = time.time() - start_time

        log_workflow(
            customer_message,
            "Failed",
            "",
            str(e),
            duration
        )

        print("\n[Workflow Error]")
        print(str(e))

        print(
            f"\n[Performance] "
            f"Workflow stopped after {duration:.2f} seconds"
        )

        return f"Workflow could not be completed: {str(e)}"


if __name__ == "__main__":

    customer_message = input(
        "\nEnter your customer request: "
    )

    run_customer_workflow(customer_message)