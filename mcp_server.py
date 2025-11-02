"""
MCP Server using FastMCP (latest style)
---------------------------------------
This server exposes:
1. A resource (`file://{path}`) that reads and returns file contents.
2. A tool (`search_file`) that searches for a keyword within that file.

Usage:
    pip install fastmcp
    fastmcp run mcp_server:app
"""

from fastmcp import FastMCP
import re
import os

# Initialize server
mcp = FastMCP(
    name="keyword_search_mcp",
    description="MCP server that searches for keywords in files via resources.",
    version="1.0.0"
)

@mcp.resource("file://{path}")
def read_file(path: str) -> str:
    """
    Resource: Reads a file from the given path and returns its text content.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")

    # Stream reading for large files
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

@mcp.tool()
def search_file(keyword: str, path: str, case_sensitive: bool = False):
    """
    Tool: Search for a specific keyword inside a file fetched via resource.
    
    Args:
        keyword: The text to search for.
        path: File path (used by the file:// resource).
        case_sensitive: Whether to treat keyword matching as case-sensitive.

    Returns:
        Dictionary with total matches and context snippets.
    """
    if not keyword or not keyword.strip():
        raise ValueError("Keyword cannot be empty or whitespace only.")
    keyword = keyword.strip()

    # Fetch file content via resource
    content = read_file(path)

    # Compile regex pattern
    flags = 0 if case_sensitive else re.IGNORECASE
    pattern = re.compile(re.escape(keyword), flags)

    occurrences = []
    for idx, line in enumerate(content.splitlines(), start=1):
        for match in pattern.finditer(line):
            start, end = match.start(), match.end()
            snippet = line[max(0, start - 40): min(len(line), end + 40)]
            occurrences.append({
                "line_number": idx,
                "start": start,
                "end": end,
                "snippet": snippet
            })

    return {
        "file": path,
        "keyword": keyword,
        "total_occurrences": len(occurrences),
        "occurrences": occurrences
    }


