import asyncio

from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from langgraph_a2a_server import A2AServer

from doc_agent import build_agent


def _agent_card() -> AgentCard:
    return AgentCard(
        name="doc_summarizer_agent",
        description="Summarizes documents from MCP resources via MCP tools.",
        version="1.0.0",
        # will expose this locally instead of contextforge to build better understanding of a2a working
        url="http://localhost:8010/",
        capabilities=AgentCapabilities(streaming=False, pushNotifications=False),
        defaultInputModes=["text/plain"],
        defaultOutputModes=["text/plain"],
        skills=[
            AgentSkill(
                id="docs.summarize",
                name="Summarize Docs",
                description="Efficiently reads/searches docs via MCP and summarizes.",
                tags=["docs", "summarize", "mcp"],
            )
        ],
    )


def main() -> None:
    # Build the LangGraph agent before starting the server.
    agent = asyncio.run(build_agent())
    agent_card = _agent_card()

    server = A2AServer(
        agent,
        serve_at_root=True,
        agent_card=agent_card,
        host="0.0.0.0",
        port=8010,
        http_url=agent_card.url,
    )

    # NOTE: `serve()` is synchronous (it calls `uvicorn.run()` internally).
    server.serve(app_type="starlette")


if __name__ == "__main__":
    # Recommended invocation (from repo root):
    #   python a2a/doc_agent_a2a_server.py
    main()


