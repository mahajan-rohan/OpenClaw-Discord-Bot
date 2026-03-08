# 🤖 OpenClaw AI Assistant (Discord Edition)

> **An autonomous, agentic Discord bot powered by Local File-System Memory, RAG (Retrieval-Augmented Generation), Groq/Llama-3, and MCP (Model Context Protocol) for GitHub.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org/)
[![Discord](https://img.shields.io/badge/Discord-discord.py-7289DA.svg)](https://discordpy.readthedocs.io/)
[![LLM](https://img.shields.io/badge/LLM-Llama--3.3--70b-orange.svg)](https://groq.com/)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
  - [High-Level Architecture](#high-level-architecture)
  - [Component Deep Dive](#component-deep-dive)
- [How It Works](#-how-it-works)
  - [Message Processing Flow](#message-processing-flow)
  - [Hybrid Memory System](#1-hybrid-memory-system-rag--core)
  - [MCP Integration](#2-mcp-model-context-protocol)
  - [Heartbeat Autonomy](#3-the-heartbeat-autonomy)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage Examples](#-usage-examples)
- [Project Structure](#-project-structure)
- [License](#-license)

---

## 🌟 Overview

OpenClaw is a production-grade, autonomous conversational AI built for Discord. Unlike standard chatbots, OpenClaw operates as a true Agent. It features a multi-layered memory architecture, intelligent tool calling, and a background "heartbeat" that allows it to operate proactively.

| System | Purpose | Technology |
|--------|---------|------------|
| **Brain** | Reasoning, Tool Orchestration, & Generation | Groq API (Llama-3.3-70b-versatile) |
| **Short-Term Memory** | Search & retrieve historical Discord messages | ChromaDB + SentenceTransformers |
| **Core Memory** | Persistent user preferences, soul, & tasks | Local Markdown File System (`.md`) |
| **Hands (MCP)** | Interact with the outside world (GitHub, Gmail) | Model Context Protocol (`npx` + `FastMCP`) |
| **Pulse** | Proactive background task execution | `asyncio` loops + `dateparser` |

---

## ✨ Features

### 🧠 Hybrid Memory Architecture
* **Vector Database (RAG):** Automatically indexes Discord conversations into ChromaDB.
* **Query Expansion:** The LLM actively brainstorms search synonyms (e.g., mapping "live" to "stay") before searching memory, completely eliminating traditional RAG "blind spots".
* **Intelligent Extractor:** A background rule-engine that listens to conversations, intercepts facts/preferences ("I hate X", "I love Y"), and routes them into permanent markdown files.

### 🔌 MCP (Model Context Protocol)
* **GitHub Integration:** * Search repositories, create issues, and read files organically.
* **Gmail Integration (Custom):** * Securely send individual or bulk emails directly from Discord using Python `FastMCP`.

### 💓 Autonomy (The Heartbeat)
* **Background Scheduler:** Runs every 60 seconds independently of user input.
* **Task Management:** Parses natural language dates in `4_heartbeat.md` using `dateparser` and proactively pings designated Discord channels when tasks are due.

---

## 🏗 Architecture

### High-Level Architecture

```text
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DISCORD SERVER                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │  #general   │  │  #dev-team  │  │    DMs      │  │  @mentions  │            │
└─────────┼────────────────┼────────────────┼────────────────┼────────────────────┘
          │                │                │                │
          ▼                ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           DISCORD.PY (Event Loop)                                │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          INTELLIGENT AGENT (Llama 3)                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                         CONTEXT ASSEMBLY                                 │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                   │   │
│  │  │   CORE (.MD) │  │   SMART RAG  │  │     MCP      │                   │   │
│  │  │   MEMORY     │  │   CONTEXT    │  │    TOOLS     │                   │   │
│  │  │              │  │              │  │              │                   │   │
│  │  │ 1_soul.md    │  │ Query Expand │  │ GitHub       │                   │   │
│  │  │ user.md      │  │ + ChromaDB   │  │ Gmail        │                   │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘                   │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
          │                         │                         │
          ▼                         ▼                         ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   VECTOR STORE   │    │  MD FILE SYSTEM  │    │   MCP SERVERS    │
│   (ChromaDB)     │    │  (memory_core/)  │    │                  │
│                  │    │                  │    │  ┌────────────┐  │
│  Short-term      │    │  • 1_soul.md     │    │  │   GitHub   │  │
│  fact indexing   │    │  • user.md       │    │  │  (Node.js) │  │
│                  │    │  • memory.md     │    │  └────────────┘  │
│  Embeddings:     │    │  • 4_heartbeat   │    │  ┌────────────┐  │
│  MiniLM-L6-v2    │    │                  │    │  │   Gmail    │  │
│                  │    │                  │    │  │  (FastMCP) │  │
└──────────────────┘    └──────────────────┘    └────────────┴─────┘
          │                         │                         │
          ▼                         ▼                         ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   LOCAL DISK     │    │   LOCAL DISK     │    │  EXTERNAL APIs   │
│   ./chroma_db/   │    │   Markdown I/O   │    │  GitHub, Google  │
└──────────────────┘    └──────────────────┘    └──────────────────┘
```

---

## 🔄 How It Works

### Message Processing Flow

When a user mentions the bot in Discord:

1.  **Passive Extraction:** If the message is a statement (not a command/question), the `IntelligentExtractor` evaluates it for user preferences ("I love coding") or facts and routes it to the appropriate Markdown file (Layer 2 or Layer 3).
2.  **Vector Indexing:** The message is split and indexed into ChromaDB for short-term semantic memory.
3.  **Query Expansion:** The Agent uses Llama 3 to generate synonyms for the user's question (e.g., "Where do I live?" -> "Where do I stay?").
4.  **Context Assembly:** The bot retrieves matches from ChromaDB and compiles them alongside the permanent Core Markdown layers.
5.  **Agent Decision:** The LLM evaluates the context and available tools. It either responds directly with text or emits a `tool_call`.
6.  **Tool Execution:** If a tool is called (e.g., `search_repositories`), the bot routes the JSON-RPC command to the MCP server, executes the action, and returns the result to Discord.

---

### 1. Hybrid Memory System (RAG + Core)

Traditional RAG fails at deep personalization. OpenClaw uses a Hybrid approach:

* **RAG (ChromaDB):** Catches exact phrases and recent contextual history. Uses `all-MiniLM-L6-v2` locally to avoid embedding API costs.
* **Core Memory (`memory_core/`):** A rigid, un-hallucinated file system. 
    * `1_soul.md`: Defines the bot's personality and instructions.
    * `user.md`: Stores extracted likes, dislikes, and passions.
    * `memory.md`: Stores biographical facts (location, job, projects).

### 2. MCP (Model Context Protocol)

MCP standardizes how the AI connects to tools. OpenClaw implements two servers:
* **Global Node.js Server (GitHub):** Spawns dynamically via Python `subprocess` interacting with the `@modelcontextprotocol/server-github` package.

### 3. The Heartbeat (Autonomy)

The `HeartbeatSystem` is an `asyncio` task loop that pulses every 60 seconds.
* It reads `4_heartbeat.md`.
* It looks for unchecked tasks `* [ ]`.
* It uses `dateparser` to interpret natural language time ("in 5 minutes", "at 4pm").
* If a task is due, it proactively sends a message to the configured `DISCORD_CHANNEL_ID` and marks the task as `* [x]`.

---

## 📦 Installation

### Prerequisites
* Python 3.10+
* Node.js & npm (for the GitHub MCP server)
* Discord Bot Token (with Message Content Intents enabled)
* Groq API Key
* GitHub Personal Access Token

### Step 1: Clone & Install Python Dependencies

```bash
git clone [https://github.com/yourusername/openclaw-discord-bot.git](https://github.com/yourusername/openclaw-discord-bot.git)
cd openclaw-discord-bot
pip install -r requirements.txt
```

*(Required core packages: `discord.py`, `groq`, `chromadb`, `sentence-transformers`, `mcp`, `dateparser`, `python-dotenv`)*

### Step 2: Install Global MCP Servers

```bash
npm install -g @modelcontextprotocol/server-github
```

### Step 3: Configure Environment

Create a `.env` file in the root directory:

```env
# Discord Settings
DISCORD_TOKEN=your_discord_bot_token_here
DISCORD_CHANNEL_ID=123456789012345678  # Channel for proactive heartbeat alerts

# AI Engine
GROQ_API_KEY=gsk_your_groq_api_key_here

# MCP Tool Credentials
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_github_token_here
GMAIL_USER=your_email@gmail.com
GMAIL_APP_PASSWORD=abcd_efgh_ijkl_mnop
```

### Step 4: Run

```bash
python -u main.py
```

**Expected Output:**
```text
Initializing OpenClaw Memory Core...
Initializing RAG Engine...
✅ AI Model Loaded & Ready.
Initializing Intelligence Layer...
Initializing Agent...
Initializing MCP Manager...
Initializing Heartbeat...
✅ Logged in as OpenClawBot
🔌 Connecting to MCP Servers (GitHub, Gmail)...
✅ Found Server Script: .../index.js
✅ Gmail Server Configured
🛠️  MCP Tools Active: 28 tools loaded.
💓 Starting Autonomy Loop...
--------------------------------------------------
🚀 OpenClaw System Online.
💓 Heartbeat System: Started.
```

---

## 💡 Usage Examples

### Natural Conversation & Memory
> **User:** I hate working in Java. I prefer Python.
> *(Bot silently extracts this to `user.md`)*
> 
> **User:** @OpenClaw What language should I write this new script in?
> **Bot:** Since you prefer Python and aren't a fan of Java, let's definitely write it in Python. Here is a starter template...

### Tool Execution (GitHub MCP)
> **User:** @OpenClaw search github repositories for "openclaw"
> **Bot:** 🛠️ **Executing Tool:** `search_repositories`...
> ✅ **Result:** *[Returns JSON data containing repo links and descriptions]*

### Proactive Autonomy (Heartbeat)
> *(Added to `4_heartbeat.md`: `* [ ] Remind me to check the server logs at 5:00 PM`)*
> *(At exactly 5:00 PM, without the user speaking)*
> **Bot:** ⏰ **REMINDER:** Remind me to check the server logs at 5:00 PM


---

## 📁 Project Structure

```text
openclaw-discord-bot/
├── main.py                     # Main execution loop and Discord events
├── config.py                   # Environment variable loading & validation
├── memory_core/                # Local Markdown Database (Auto-generated)
│   ├── 1_soul.md               # Base personality
│   ├── user.md                 # User preferences
│   ├── memory.md               # User facts
│   └── 4_heartbeat.md          # Scheduled tasks
├── src/
│   ├── brain/
│   │   ├── agent.py            # Llama 3 Router, Tool Calling, Query Expansion
│   │   └── prompt_builder.py   # Assembles system prompts from Markdown
│   ├── memory_system/
│   │   ├── file_manager.py     # I/O for Markdown files
│   │   ├── extractor.py        # Intercepts rules to update Core Memory
│   │   └── scheduler.py        # Heartbeat loop & date parsing
│   ├── rag_engine/
│   │   ├── vector_store.py     # ChromaDB initialization & embedding
│   │   └── indexer.py          # Message splitting and Vector Search logic
│   └── mcp/
│       ├── manager.py          # Client connection handling
│       ├── server_config.py    # Subprocess definitions for MCP servers
│       ├── client.py           # Standard stdio MCP Client wrapper
│       └── gmail_server.py     # Custom FastMCP Python server
├── .env                        # Environment variables
└── requirements.txt            # Python dependencies
```

