from agent.agent import Agent


agent = Agent()

print("=== AI RESEARCH AGENT ===")
print("Type 'quit' to exit.")

while True:

    user_input = input("\nYou: ")

    if user_input.lower() in ["quit", "exit"]:
        print("Goodbye!")
        break

    try:
        result = agent.run(user_input)

        if result["type"] == "research":
            print("\nGemini: Research completed.")

            topic = result["topic"]
            sources = result["results"]

            report = f"# Research Report: {topic}\n\n"

            report += "## Sources\n\n"

            for i, source in enumerate(sources, 1):
                report += f"### {i}. {source['title']}\n"
                report += f"URL: {source['url']}\n"
                report += f"Score: {source['score']}\n\n"
                report += f"{source['content']}\n\n"

            with open("reports/research_report.md", "w", encoding="utf-8") as f:
                f.write(report)

            print(f"[REPORT SAVED] reports/research_report.md")

        elif result["type"] == "time":
            print(f"\nCurrent time: {result['value']}")

        elif result["type"] == "calculator":
            print(f"\nResult: {result['result']}")

        elif result["type"] == "error":
            print(f"\n[ERROR] {result['message']}")

        else:
            print(f"\nGemini: {result['content']}")

    except Exception as e:
        print(f"\n[ERROR] {e}")
