# app/api/v1/chat.py
from fastapi import APIRouter, Depends
from langchain_core.messages import HumanMessage
from app.schemas.response import ResponseModel
from app.schemas.agent import MessageIn
from app.models.models import User
from app.dependencies import (
    get_current_user,
)
from app.utils.response import ok
from uuid import uuid4
from app.agents.State import WorkState
from app.agents.router import workflow

auth_router = APIRouter(
    prefix="/chat",
    tags=["对话API"],
)


@auth_router.post(path="/message", response_model=ResponseModel[str])
async def chat(
    message : MessageIn,
    current_user : User = Depends(get_current_user),
) -> ResponseModel[str]:
    """
    与智能体进行对话交互。

    客户端提交一条消息，智能体根据上下文和工具调用生成回复。
    目前仅支持单轮对话，后续将增加多轮上下文记忆功能。

    Args:
        message: 包含用户输入内容的 MessageIn 模型。

    Returns:
        统一响应包装，data 字段为智能体生成的回复字符串。
    """
    config = {
        "configurable" : {
            "thread_id" : uuid4(),
        }
    }
    response = await workflow.ainvoke(input=WorkState(
        context=message.message, 
        user_id=current_user.id,
        notes=[],
        categories=[],
        config=config,
        output=""
        ),
    )
    print(response)
    return ok(data=response.get("output", ""), message="对话成功")
