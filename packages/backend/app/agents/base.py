from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, ToolMessage
from app.agents.tools.time import get_current_time_tool

llm = ChatOpenAI(
    model="deepseek-chat",  # 用 deepseek-chat 即可
    api_key="sk-5adb72a0000c4e9994a4cfdf93f950a1",
    base_url="https://api.deepseek.com/v1",
)

# llm = ChatOpenAI(
#     model="glm-4.5-flash",  # 用 deepseek-chat 即可
#     api_key="b8f3bb41a18342bbaabbe9c893d20854.P2gv0RnHJMqcWv5w",
#     base_url="https://open.bigmodel.cn/api/paas/v4/",
# )
