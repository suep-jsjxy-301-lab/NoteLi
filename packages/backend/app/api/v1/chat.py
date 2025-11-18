# app/api/v1/chat.py
from fastapi import APIRouter

from app.agents.router import knowledge_workflow

auth_router = APIRouter(
    prefix="/chat",
    tags=["对话API"],
)


@auth_router.post("/")
async def get_chat():
    response = knowledge_workflow.astream({"input": "帮我整理项目管理相关的知识"})
    return {"message": response}

    # return {"message": "Chat endpoint is working."}
