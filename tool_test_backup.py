import os
from datetime import datetime

from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def get_current_time():
    """Return the current local date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculate(a: float, b: float, operation: str):
    """Perform a basic mathematical calculation."""

    print(f"\n[TOOL CALLED] calculate(a={a}, b={b}, operation='{operation}')")

    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            result = "Cannot divide by zero"
        else:
            result = a / b
    else:
        result = "Unknown operation"

    print(f"[TOOL RESULT] {result}")

    return result

def research(topic: str):
    """Research a topic and return basic research information."""

    print(f"\n[TOOL CALLED] research(topic='{topic}')")

    result = f"""
Research topic: {topic}

Key areas to investigate:
1. What is {topic}?
2. How does {topic} work?
3. Real-world examples of {topic}
4. Practical applications of {topic}
5. Important concepts for beginners
"""

    print(f"[TOOL RESULT]\n{result}")

    return result

chat = client.chats.create(
    model="gemini-3.5-flash-lite",
    config={
        "tools": [get_current_time, calculate, research]
    }
)


while True:
    user_input = input("\nYou: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    response = chat.send_message(user_input)

    print("\nGemini:", response.text)