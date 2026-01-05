import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

load_dotenv()

llm = init_chat_model(
    model="gpt-4o-mini",
    model_provider="openai",
    api_key=os.getenv("LITELLM_API_KEY"),
    base_url=os.getenv("LITELLM_URL"),
)
MCP_URL = os.getenv("DOCS_MCP_URL")


async def build_agent():
    if not MCP_URL:
        raise RuntimeError(
            "DOCS_MCP_URL is not set. Example: set DOCS_MCP_URL as e.g: http://localhost:8000/sse"
        )
    # 1) Connect to MCP server by URL
    gateway_token = os.getenv("GATEWAY_TOKEN")
    headers = {"Authorization": f"Bearer {gateway_token}"} if gateway_token else {}

    client = MultiServerMCPClient(
        {
            "docs": {
                "url": MCP_URL,
                "transport": "sse",
                **({"headers": headers} if headers else {}),
            }
        }
    )

    # 2) Load MCP tools and convert to LangChain tools
    tools = await client.get_tools()
    print(f"Tools: {tools}")

    # 3) Fully autonomous ReAct agent
    return create_react_agent(
        model=llm,
        tools=tools,
        prompt=(
            "You are DocSummarizer.\n"
            "Use MCP tools to list/read/search documents.\n"
            "Be efficient: search first, then read only necessary docs.\n"
            "Return concise summaries and key bullet points.\n"
        ),
    )


