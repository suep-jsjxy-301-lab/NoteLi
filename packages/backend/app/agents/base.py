import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from app.agents.State import ContextState, AgentState
from .tools.time import get_current_time_tool
from .tools.note import create_note_tool, update_note_tool, search_notes_tool, delete_note_tool
from .tools.category import create_category_tool, update_category_tool, delete_category_tool, search_categories_tool, get_default_icon_tool
from app.agents.middleware.prompt import get_dynamic_prompt, get_chat_prompt

load_dotenv("../../.env")

checkpointer = InMemorySaver()

tools = [get_current_time_tool, 
        create_note_tool, update_note_tool, search_notes_tool, delete_note_tool,
        create_category_tool, update_category_tool, delete_category_tool, search_categories_tool, get_default_icon_tool,
        ]

middleware = [get_dynamic_prompt]

llm = ChatOpenAI(
    model=os.getenv("MODEL"),
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL"),
    model_kwargs={
        "extra_body": {
            "thinking": {"type": "disabled"} # 核心：关闭思考模式
        }
    }
)

agent = create_agent(
    model = llm,
    tools = tools,
    middleware = middleware,
    state_schema = AgentState,
    context_schema = ContextState,
    checkpointer = checkpointer,
)

chat_agent = create_agent(
    model = llm,
    middleware=[get_chat_prompt]
)