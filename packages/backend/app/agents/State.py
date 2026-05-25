from dataclasses import dataclass
from typing import Annotated, List, Optional, TypedDict
from uuid import UUID
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from pydantic import Field
from app.agents.model import NoteModel, CategoryModel
from app.models.models import User

@dataclass
class Taskstep :
    name: str
    description: str

# Graph state
class WorkState(TypedDict):
    notes : list[NoteModel] = Field(default_factory=list)  # 用于存储选中笔记
    categories : list[CategoryModel] = Field(default_factory=list) # 用于存储选中分类
    steps: list[Taskstep] = Field(default_factory=list)  # 用于存储任务步骤
    work: list[Taskstep] = Field(default_factory=list)  # 用于存储执行的任务
    context: str  # 用于存储检索到的上下文
    user_id : UUID  # 用于存储用户信息
    config: dict = Field(default_factory=dict)  # 用于存储智能体配置，如用户信息、线程ID等
    output: Optional[str] = None  # 用于存储智能体的输出结果

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

class ContextState(TypedDict):
    user_id : UUID
    step: Taskstep # 当前步骤
    notes : list[NoteModel] = Field(default_factory=list)  # 用于存储选中笔记
    categories : list[CategoryModel] = Field(default_factory=list) # 用于存储选中分类