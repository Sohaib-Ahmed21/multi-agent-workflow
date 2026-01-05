# Multi-agent-workflow

Simple end-to-end **multi-agent workflow** using **MCP** (tools/resources) + **A2A** (agent server) + a small **orchestrator** that can call the A2A agent as a tool.

## Prereqs

- Python **3.11+**
- [Poetry](https://python-poetry.org/)
- An LLM endpoint configured via env vars (this repo uses `gpt-4o-mini` via LiteLLM-style vars)

## Environment variables

This project uses `python-dotenv` (`load_dotenv()`), so you can set these in your shell or in a `.env` file in the repo root.

- **Required**
  - `LITELLM_API_KEY`: API key for your LLM provider / LiteLLM
  - `LITELLM_URL`: base URL for the LLM endpoint (e.g., your LiteLLM proxy)
  - `DOCS_MCP_URL`: MCP SSE endpoint URL  
    - Local example: `http://localhost:8000/sse`
- **Optional**
  - `GATEWAY_TOKEN`: Bearer token if you are routing MCP through ContextForge Gateway with auth

## Run (commands in sequence)

Run these from the repo root **in order**. (Keep the Gateway, MCP server, and A2A server running in separate shells.)

### 1) Install dependencies

```bash
poetry install
```

### 2) Activate the Poetry virtual environment

```bash
poetry env activate
```

### 3) Start ContextForge Gateway (local)

```bash
poetry run mcpgateway
```

### 4) Start the MCP server (docs tools/resources)

```bash
python mcp/doc_mcp_server.py
```

- MCP runs SSE on `http://localhost:8000/sse`
- The docs are in `mcp/docs/` (example: `coding_docs.md`)

### 5) Start the A2A agent server

```bash
python a2a/doc_agent_a2a_server.py
```

- A2A agent server runs on `http://localhost:8010/`

### 6) Run the orchestrator (interactive chat)

```bash
python orchestrator.py
```

Now **chat in this terminal**. Type `exit` or `quit` to end the session.

## Notes (ContextForge Gateway + Keycloak)

- If you serve MCP tools via **ContextForge Gateway**, set `DOCS_MCP_URL` to your gateway’s SSE URL and set `GATEWAY_TOKEN` to a valid Bearer token.
- If your gateway is protected via **Keycloak** (IdP), obtain a token from Keycloak and use it as `GATEWAY_TOKEN`.


