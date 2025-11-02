"""
MCP Server: Keyword Search
--------------------------
This server exposes:
1. A resource (`file://{path}`) that reads and returns file contents.
2. A tool (`search_file`) that searches for a keyword within that file.
"""

from fastmcp import FastMCP
import re
import os

# Initialize MCP server
mcp = FastMCP(name="keyword_search_mcp")

@mcp.resource("file://{path}")
def read_file(path: str) -> str:
    """
    Resource: Reads a file from the given path and returns its text content.
    """
    file_path = os.path.abspath(path)
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Stream read (handles large files gracefully)
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

@mcp.tool()
def search_file(keyword: str, path: str, case_sensitive: bool = False):
    """
    Tool: Search for a specific keyword inside a file.
    
    Args:
        keyword: The text to search for.
        path: File path to search in.
        case_sensitive: Whether to treat keyword matching as case-sensitive.

    Returns:
        Dictionary with total matches and context snippets.
    """
    if not keyword or not keyword.strip():
        raise ValueError("Keyword cannot be empty or whitespace only.")
    keyword = keyword.strip()

    # Read the file directly
    file_path = os.path.abspath(path)
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Compile regex
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

if __name__ == "__main__":
    mcp.run()