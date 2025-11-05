from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
import asyncio
from agents.agent import init_agent

# 定义请求模型
class QuestionRequest(BaseModel):
    question: str

# 定义响应模型
class AnswerResponse(BaseModel):
    answer: str

# 全局变量
agent = None

@asynccontextmanager
async def lifespan(_app: FastAPI):
    global agent
    # 启动时运行
    agent = await init_agent()
    yield
    # 关闭时清理（可选）
    agent = None

app = FastAPI(
    title="LangChain FastAPI集成示例",
    version="0.0.1",
    lifespan=lifespan
)

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """处理用户问题并返回LangChain生成的答案"""
    global agent
    if agent is None:
        return AnswerResponse(answer="智能体尚未初始化，请稍后再试")
    
    try:
        result = agent.invoke(
            {"messages": [{"role": "user", "content": request.question}]}
        )
        # 根据返回结果，现在返回的是包含 messages 的字典
        # 需要获取最后一个 AI 消息的内容
        if isinstance(result, dict) and "messages" in result:
            messages = result["messages"]
            if messages and len(messages) > 0:
                # 获取最后一个消息（应该是 AI 的回复）
                last_message = messages[-1]
                # 检查是否是 AIMessage 并提取内容
                if hasattr(last_message, 'content'):
                    return AnswerResponse(answer=last_message.content)
                else:
                    return AnswerResponse(answer=str(last_message))
            else:
                return AnswerResponse(answer="未收到有效回复")
        elif isinstance(result, dict):
            # 尝试访问常见的键名
            if "text" in result:
                return AnswerResponse(answer=result["text"])
            elif "output" in result:
                return AnswerResponse(answer=result["output"])
            elif "content" in result:
                return AnswerResponse(answer=result["content"])
            else:
                # 如果没有找到常见键，返回整个结果的字符串表示
                return AnswerResponse(answer=str(result))
        else:
            # 如果结果不是字典，直接返回字符串表示
            return AnswerResponse(answer=str(result))
    except Exception as e:
        return AnswerResponse(answer=f"处理请求时出错：{str(e)}")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
