from tools.research import research
from tools.calculator import add, subtract, multiply, divide
from tools.time import get_current_time


class Agent:
    def __init__(self):
        self.name = "AI Research Assistant"

    def run(self, message: str):
        message = message.strip()

        # -------------------------
        # Research
        # -------------------------
        if message.lower().startswith("research:"):
            topic = message.split(":", 1)[1].strip()

            results = research(topic)

            return {
                "type": "research",
                "topic": topic,
                "results": results,
            }

        # Natural language research command
        if message.lower().startswith("research "):
            topic = message.split(" ", 1)[1].strip()

            results = research(topic)

            return {
                "type": "research",
                "topic": topic,
                "results": results,
            }

        # -------------------------
        # Current time
        # -------------------------
        if message.lower() == "time":
            return {
                "type": "time",
                "value": get_current_time(),
            }

        # -------------------------
        # Calculator
        # -------------------------
        if message.lower().startswith("calculate:"):
            parts = message.split(":", 1)[1].strip()

            try:
                a, op, b = parts.split()

                a = float(a)
                b = float(b)

                if op == "+":
                    result = add(a, b)
                elif op == "-":
                    result = subtract(a, b)
                elif op == "*":
                    result = multiply(a, b)
                elif op == "/":
                    result = divide(a, b)
                else:
                    raise ValueError("Unsupported operator")

                return {
                    "type": "calculator",
                    "result": result,
                }

            except Exception as e:
                return {
                    "type": "error",
                    "message": str(e),
                }

        # -------------------------
        # Default
        # -------------------------
        return {
            "type": "message",
            "content": (
                f"Hello! I am {self.name}. "
                "Try 'Research <topic>', 'time', "
                "or 'calculate: 5 + 3'"
            ),
        }
