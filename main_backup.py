import os
from datetime import datetime

from dotenv import load_dotenv
from google import genai


# -----------------------------
# Load API key
# -----------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)


# -----------------------------
# Tool 1: Current time
# -----------------------------

def get_current_time():
    """Return the current local date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# -----------------------------
# Tool 2: Calculator
# -----------------------------

def calculate(a: float, b: float, operation: str):
    """Perform a basic mathematical calculation."""

    print(
        f"\n[TOOL CALLED] calculate("
        f"a={a}, b={b}, operation='{operation}')"
    )

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


# -----------------------------
# Create AI chat
# -----------------------------

chat = client.chats.create(
    model="gemini-3.5-flash-lite",
    config={
        "tools": [
            get_current_time,
            calculate,
        ]
    }
)


# -----------------------------
# Research Agent
# -----------------------------

print("=== AI RESEARCH AGENT ===")
print("Type 'quit' to exit.")

while True:

    user_input = input("\nYou: ")

    if user_input.lower() in ["quit", "exit"]:
        print("Goodbye!")
        break

    response = chat.send_message(user_input)

    print("\nGemini:", response.text)