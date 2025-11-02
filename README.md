# 🔍 Keyword Search MCP Server

An **MCP (Model Context Protocol)** server built with **FastMCP**, enabling file reading and keyword search through registered tools and resources.

---

## 🚀 Features

* **File Resource:** Reads and returns file contents
* **Search Tool:** Finds keywords in text files with context snippets
* **Case-sensitive toggle:** Supports flexible search modes
* **Lightweight & Async:** Uses FastMCP async resources/tools

---

## ⚙️ Installation

```bash
pip install fastmcp
```

---

## 🖥️ Usage

### Start the Server

```bash
python keyword_search_mcp.py
```

### Resources

**`file://{path}`** — Reads text files
Example: `file:///home/user/contracts.txt`

### Tools

**`search_file`** — Searches for a keyword inside a file
**Parameters:**

| Name             | Type   | Required | Description                        |
| ---------------- | ------ | -------- | ---------------------------------- |
| `keyword`        | string | ✅        | Word to search                     |
| `path`           | string | ✅        | File path                          |
| `case_sensitive` | bool   | ❌        | Case match toggle (default: False) |

**Returns:**
`file`, `keyword`, `total_occurrences`, and a list of `occurrences` with line numbers and snippets.

---

## 📄 Example

**Request:**

```json
{
  "keyword": "Agreement",
  "path": "contracts.txt",
  "case_sensitive": false
}
```

**Response:**

```json
{
  "file": "contracts.txt",
  "keyword": "Agreement",
  "total_occurrences": 3,
  "occurrences": [
    {
      "line_number": 1,
      "start": 12,
      "end": 21,
      "snippet": "MASTER SERVICE AGREEMENT"
    }
  ]
}
```

---

## ⚠️ Limitations

* **Text files only** (`.txt`, `.md`, `.log`, etc.)
* **Recommended max file size:** 10 MB (reads entire file into memory)
* **No fuzzy search:** Exact substring matching only
* **UTF-8 encoding:** Non-UTF-8 characters replaced safely

---

## 🧠 Error Handling

| Error                | Description                                   |
| -------------------- | --------------------------------------------- |
| `FileNotFoundError`  | File does not exist                           |
| `ValueError`         | Empty or invalid keyword                      |
| `PermissionError`    | Access denied                                 |
| `UnicodeDecodeError` | Non-text file (auto-handled with replacement) |

---
