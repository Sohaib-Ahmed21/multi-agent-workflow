from __future__ import annotations

from pathlib import Path

from fastmcp import FastMCP

mcp = FastMCP("docs-mcp")

# Use a path relative to this file (not the current working directory).
DOCS_DIR = Path(__file__).resolve().parent / "docs"


# ---- Internal helpers (plain functions; safe to call from tools/resources) ----
def _list_docs() -> str:
    files = sorted(p.name for p in DOCS_DIR.glob("*.md"))
    return "\n".join(files) if files else "No docs found."


def _read_doc(name: str) -> str:
    path = DOCS_DIR / name
    if not path.exists():
        return f"Not found: {name}"
    return path.read_text(encoding="utf-8")


def _search_docs(query: str) -> str:
    q = query.strip()
    if not q:
        return "Query was empty."

    hits: list[str] = []
    for p in sorted(DOCS_DIR.glob("*.md")):
        try:
            lines = p.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue

        matches: list[str] = []
        for i, line in enumerate(lines, start=1):
            if q.lower() in line.lower():
                matches.append(f"{i}: {line}")

        if matches:
            hits.append(f"== {p.name} ==\n" + "\n".join(matches[:50]))

    return "\n\n".join(hits) if hits else "No matches."


# ---- Resources: documents live here ----
@mcp.resource("docs://list")
def list_docs_resource() -> str:
    return _list_docs()


@mcp.resource("docs://{name}")
def get_doc_resource(name: str) -> str:
    return _read_doc(name)


# ---- Tools: minimal access layer to resources ----
@mcp.tool()
def list_docs() -> str:
    "List available document names."
    return _list_docs()


@mcp.tool()
def read_doc(name: str) -> str:
    "Read a document by name."
    return _read_doc(name)


@mcp.tool()
def search_docs(query: str) -> str:
    "Search all documents for a query and return matching snippets."
    return _search_docs(query)


if __name__ == "__main__":
    # IMPORTANT: run with HTTP/SSE so clients can connect by URL
    mcp.run(transport="sse", host="0.0.0.0", port=8000)


