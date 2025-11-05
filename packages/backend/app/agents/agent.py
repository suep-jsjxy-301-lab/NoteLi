# app/agents/agent.py
import os
import asyncio

from dotenv import load_dotenv
from pydantic import SecretStr

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

raw_key = os.getenv("DEEPSEEK_API_KEY")
if not raw_key:
    raise RuntimeError("API_KEY 没有在 .env 里配置")

# glm_key = os.getenv("GLM_API_KEY")
# if not glm_key:
#     raise RuntimeError("API_KEY 没有在 .env 里配置")

llm = ChatOpenAI(
    model="deepseek-chat",
    # stream_usage=True,
    # temperature=None,
    # max_tokens=None,
    # timeout=None,
    # reasoning_effort="low",
    # max_retries=2,
    api_key=SecretStr(raw_key),
    base_url="https://api.deepseek.com",
    # organization="...",
    # other params...
)
# glm_flash = ChatOpenAI(
#     model="glm-4.5-flash",
#     # stream_usage=True,
#     # temperature=None,
#     # max_tokens=None,
#     # timeout=None,
#     # reasoning_effort="low",
#     # max_retries=2,
#     api_key=SecretStr(glm_key),
#     base_url="https://open.bigmodel.cn/api/coding/paas/v4",
#     # organization="...",
#     # other params...
# )


client = MultiServerMCPClient(
    {
        "bing-cn-mcp-server": {
            "transport": "sse",  # HTTP-based remote server
            # Ensure you start your weather server on port 8000
            "url": "https://mcp.api-inference.modelscope.net/ddcd6c8bb1a341/sse",
        },
    }
)


def get_weather(city: str) -> str:
    """Get weather for a given city."""

    return f"It's always sunny in {city}!"


# agent = create_agent(
#     model=llm,
#     # tools=tools,
#     tools=[get_weather],
#     system_prompt="你是一个默认用中文回答的智能体",
# )

tools = asyncio.run(client.get_tools())
agent = create_agent(
    model=llm,
    tools=[get_weather] + tools,
    system_prompt="你是一个默认用中文回答的智能体",
)