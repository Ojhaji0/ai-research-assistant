from agent.agent import Agent


def main():
    agent = Agent()

    print("=== AI RESEARCH AGENT ===")
    print("Type 'quit' to exit.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break

        if not user_input:
            continue

        try:
            result = agent.run(user_input)

            print(f"\nGemini: {result['content']}")

            if result["type"] == "research":
                print(f"[REPORT SAVED] {result['report_path']}")

        except Exception as e:
            print(f"\n[ERROR] {e}")


if __name__ == "__main__":
    main()