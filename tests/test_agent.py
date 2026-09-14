from unittest.mock import MagicMock, patch

import pytest

from agent.agent import Agent


SAMPLE_SOURCES = [
    {
        "title": "AI Research Source",
        "url": "https://example.com/ai",
        "content": "Sample AI research content.",
        "score": 4.5,
    },
    {
        "title": "Agent Research Source",
        "url": "https://example.edu/agents",
        "content": "Sample agent research content.",
        "score": 4.2,
    },
]


@pytest.fixture
def mock_client():
    with patch("agent.agent.genai.Client") as mock:
        client = mock.return_value
        client.chats.create.return_value = MagicMock()
        yield mock, client


def test_agent_init_missing_api_key():
    with patch.dict("os.environ", {}, clear=True):
        with patch("agent.agent.genai.Client"):
            with pytest.raises(
                ValueError,
                match="GEMINI_API_KEY not found in .env file",
            ):
                Agent()


def test_agent_init_registers_tools(mock_client):
    _, client = mock_client

    with patch.dict(
        "os.environ",
        {"GEMINI_API_KEY": "test-key"},
        clear=False,
    ):
        Agent()

    client.chats.create.assert_called_once()

    call_kwargs = client.chats.create.call_args.kwargs
    config = call_kwargs["config"]

    tools = config.tools

    assert len(tools) == 3

    tool_names = {tool.__name__ for tool in tools}

    assert "research_tool" in tool_names
    assert "get_current_time" in tool_names
    assert "calculate" in tool_names


def test_agent_run_normal_message(mock_client):
    _, client = mock_client

    mock_chat = client.chats.create.return_value
    mock_chat.send_message.return_value = MagicMock(
        text="Hello there!"
    )

    with patch.dict(
        "os.environ",
        {"GEMINI_API_KEY": "test-key"},
        clear=False,
    ):
        agent = Agent()

    result = agent.run("Hello")

    assert result == {
        "type": "message",
        "content": "Hello there!",
    }

    assert agent.last_research is None

    mock_chat.send_message.assert_called_once_with("Hello")


def test_agent_run_research_flow_captures_state_and_generates_report(
    mock_client,
):
    _, client = mock_client

    mock_chat = client.chats.create.return_value

    with patch.dict(
        "os.environ",
        {"GEMINI_API_KEY": "test-key"},
        clear=False,
    ):
        with patch(
            "agent.agent.planned_research",
            return_value=SAMPLE_SOURCES,
        ) as mock_research:
            with patch(
                "agent.agent.generate_research_report",
                return_value="reports/research_report.md",
            ) as mock_generate_report:

                agent = Agent()

                # Find the research wrapper registered with Gemini.
                tools = client.chats.create.call_args.kwargs[
                    "config"
                ].tools

                research_tool = next(
                    tool
                    for tool in tools
                    if tool.__name__ == "research_tool"
                )

                # Simulate Gemini AFC invoking the tool during send_message.
                def simulate_afc(message):
                    research_tool("AI agent architecture")
                    return MagicMock(text="Here is the research summary.")

                mock_chat.send_message.side_effect = simulate_afc

                result = agent.run(
                    "Research AI agent architecture"
                )

    assert agent.last_research == {
        "topic": "AI agent architecture",
        "sources": SAMPLE_SOURCES,
    }

    assert result["type"] == "research"
    assert result["content"] == "Here is the research summary."
    assert result["report_path"] == "reports/research_report.md"

    mock_research.assert_called_once_with(
        "AI agent architecture"
    )

    mock_generate_report.assert_called_once_with(
        "AI agent architecture",
        SAMPLE_SOURCES,
    )


def test_agent_run_api_error_handling(mock_client):
    _, client = mock_client

    mock_chat = client.chats.create.return_value

    error = RuntimeError("Gemini API unavailable")

    mock_chat.send_message.side_effect = error

    with patch.dict(
        "os.environ",
        {"GEMINI_API_KEY": "test-key"},
        clear=False,
    ):
        agent = Agent()

    result = agent.run("Hello")

    assert result == {
        "type": "error",
        "content": "Something went wrong: Gemini API unavailable",
    }

    assert agent.last_research is None