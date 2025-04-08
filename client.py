import os
import asyncio

from openai import AsyncOpenAI
from agents import Agent, Runner, gen_trace_id, trace
from agents import set_default_openai_client, set_default_openai_api, set_tracing_disabled, set_tracing_export_api_key
from agents.mcp import MCPServer, MCPServerStdio

from dotenv import load_dotenv

load_dotenv()

"""This example uses a custom provider for all requests by default. We do three things:
1. Create a custom client.
2. Set it as the default OpenAI client, and don't use it for tracing.
3. Set the default API as Chat Completions, as most LLM providers don't yet support Responses API.

Note that in this example, we disable tracing under the assumption that you don't have an API key
from platform.openai.com. If you do have one, you can either set the `OPENAI_API_KEY` env var
or call set_tracing_export_api_key() to set a tracing specific key.
"""
# DeepSeek-V3
# client = AsyncOpenAI(base_url="https://api.deepseek.com", api_key=os.getenv('DEEPSEEK_API_KEY'))
# set_default_openai_client(client=client, use_for_tracing=False)
# set_default_openai_api("chat_completions")
# set_tracing_disabled(disabled=True)
# set_tracing_export_api_key(api_key=os.getenv('OPENAI_API_KEY'))


async def run(mcp_server: MCPServer):
    agent = Agent(
        name="Assistant",
        instructions="使用工具接入地图服务，实现查找周边地点、 规划出行路线等。",
        model="gpt-4o-2024-11-20",
        # model="deepseek-chat",
        mcp_servers=[mcp_server]
    )

    message = "北京到深圳的距离？"
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)


async def main():
    async with MCPServerStdio(
            name="baidu-map",
            params={
                "command": "uv",
                "args": [
                    "run",
                    "--with",
                    "mcp[cli]",
                    "mcp",
                    "run",
                    "baidu_map_mcp_server/map.py"
                ]
            },
    ) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name="MCP Baidu Maps Example", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/{trace_id}\n")
            await run(server)


if __name__ == "__main__":
    asyncio.run(main())
