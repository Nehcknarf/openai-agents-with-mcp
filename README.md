# OpenAI Agents SDK with MCP (Baidu Maps MCP Server)

## System Requirements
- Latest version of uv installed

## Setting Up Your Environment
```bash
cd openai-agents-with-mcp
# Install Python 3.13
uv python install 3.13
# Initialize project
uv init
# Create virtual environment
uv venv
# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Unix or MacOS:
source .venv/bin/activate
# Install required packages
uv add openai-agents "mcp[cli]"
# Remove boilerplate files
rm main.py
```
## Setting Up Your API Key
1. Create .env file
2. Add your api keys to the .env file:
```
OPENAI_API_KEY=sk-...
DEEPSEEK_API_KEY=sk-...
BAIDU_MAPS_API_KEY=...
```
