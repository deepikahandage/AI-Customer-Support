from google import genai

API_KEY = "PASTE_YOUR_NEW_GEMINI_KEY_HERE"

client = genai.Client(api_key=API_KEY)


def business_coordination_agent(user_input):

    prompt = f"""
You are an AI Business Coordination and Decision Support Agent.

You perform multiple specialized roles internally.

ROLE 1 - PLANNING:
Break the user's business problem into clear steps.

ROLE 2 - RESEARCH:
Identify the information and facts required to understand the problem.

ROLE 3 - ANALYSIS:
Analyse the available information, identify the main issue,
possible causes, risks and important factors.

ROLE 4 - DECISION SUPPORT:
Compare possible solutions and recommend the most suitable action.
Explain why the recommendation is appropriate.

ROLE 5 - RESPONSE GENERATION:
Give the user a clear, polite and professional final response.

You can also handle:
- Customer support
- Order problems
- Refund and return requests
- Business complaints
- General business decisions
- Recommendations

IMPORTANT:
Do not claim that an actual refund, order change or business action
has been completed. Give recommendations unless an external system
is connected.

User's request:
{user_input}

Follow these steps internally:
1. Understand the request.
2. Plan the solution.
3. Identify required information.
4. Analyse the situation.
5. Evaluate possible options.
6. Recommend the best action.
7. Give the final response.

Final response:
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text


def main():

    print("=" * 60)
    print("       AI BUSINESS COORDINATION AGENT")
    print("=" * 60)

    print("\nThis agent provides:")
    print("- Planning")
    print("- Research")
    print("- Analysis")
    print("- Decision Support")
    print("- Customer & Business Support")
    print("\nType 'exit' to stop.")

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        try:

            answer = business_coordination_agent(user_input)

            print("\nAI Agent:")
            print(answer)

        except Exception as e:

            print("\nError:", e)


if __name__ == "__main__":
    main()