from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langgraph_a2a_client import A2AClientToolProvider
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", 
    api_key=os.getenv("LITELLM_API_KEY"),
    base_url=os.getenv("LITELLM_URL"),
    )

DOC_AGENT_URL = "http://localhost:8010"

# This will be used to discover the agents and their tools.
provider = A2AClientToolProvider(known_agent_urls=[DOC_AGENT_URL])
tools = provider.tools

orchestrator = create_react_agent(
    model=llm,
    tools=tools,
    prompt=(
        # TENTATIVE PROMPT
        "You are an orchestrator.\n"
        "ONLY call doc_summarizer_agent if the user asks about python coding questions.\n"
        "If not python coding related, answer directly and do not call tools.\n"
        # Adding the below prompt to the orchestrator agent to ensure that the agent only
        # uses the discovered agents.
        "Don't override the discovery agent url. The strict requirement is that only use discovered agents."
    )
)

async def main():
    while True:
        q = input("\nUser> ").strip()
        if q in ("exit", "quit"):
            break
        out = await orchestrator.ainvoke({"messages": [("user", q)]})
        print("\nAssistant>", out["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
