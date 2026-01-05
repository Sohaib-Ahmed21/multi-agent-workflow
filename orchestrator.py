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

ORCHESTRATOR_PROMPT = (
    "You are an orchestrator.\n"
    "Only call doc_summarizer_agent when the user asks Python coding questions.\n"
    "Otherwise, answer directly and do not call any tools.\n"
    "Do not override the discovered agent URL; strictly use only discovered agents.\n"
)

orchestrator = create_react_agent(
    model=llm,
    tools=tools,
    prompt=ORCHESTRATOR_PROMPT,
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
