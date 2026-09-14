import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools.research import planned_research
from tools.calculator import calculate
from tools.time import get_current_time
from reports.report_generator import generate_research_report


load_dotenv()


class Agent:
    def __init__(self):
        self.name = "AI Research Assistant"
        self.last_research = None

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")

        self.client = genai.Client(api_key=api_key)

        def research_tool(topic: str):
            """Search the web using a planned multi-query research pipeline."""

            sources = planned_research(topic)

            self.last_research = {
                "topic": topic,
                "sources": sources,
            }

            return sources

        self.chat = self.client.chats.create(
            model="gemini-3.5-flash-lite",
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are an AI Research Assistant. "
                    "Use the available tools when appropriate. "
                    "Use the research tool for web research questions. "
                    "Use the calculator tool for mathematical calculations. "
                    "Use the time tool when the user asks for the current time. "
                    "For normal conversation, respond directly."
                ),
                tools=[
                    research_tool,
                    get_current_time,
                    calculate,
                ],
            ),
        )

    def run(self, message: str):
        self.last_research = None

        try:
            response = self.chat.send_message(message)

            if self.last_research:
                report_path = generate_research_report(
                    self.last_research["topic"],
                    self.last_research["sources"],
                )

                return {
                    "type": "research",
                    "content": response.text,
                    "report_path": report_path,
                }

            return {
                "type": "message",
                "content": response.text,
            }

        except Exception as e:
            return {
                "type": "error",
                "content": f"Something went wrong: {e}",
            }