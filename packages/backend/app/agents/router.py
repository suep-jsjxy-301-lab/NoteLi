# app/agents/router.py
from typing_extensions import Literal, TypedDict
from pydantic import BaseModel, Field
from langchain.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END


from app.agents.base import llm


class Route(BaseModel):
    step: Literal["search", "summarize", "organize", "qa", "extract"] = Field(
        None, description="The next step in the routing process"
    )


# Graph state
class State(TypedDict):
    input: str
    decision: str
    output: str
    context: str  # 用于存储检索到的上下文


# 建议的智能体节点：


def knowledge_search_agent(state: State):
    """搜索知识库内容"""
    # 这里可以集成向量数据库搜索
    # 示例：搜索相关笔记和文档
    search_query = state["input"]
    # 实际实现中这里会调用向量数据库
    result = llm.invoke(f"搜索知识库中关于: {search_query}")
    return {"output": result.content, "context": "检索到的相关内容..."}


def content_summarize_agent(state: State):
    """总结知识内容"""
    # 对长文档或多个笔记进行总结
    content = state.get("context", state["input"])
    result = llm.invoke(f"请总结以下内容: {content}")
    return {"output": result.content}


def knowledge_organize_agent(state: State):
    """整理和组织知识结构"""
    # 分类、打标签、建立关联
    content = state.get("context", state["input"])
    result = llm.invoke(f"请整理并组织以下知识内容: {content}")
    return {"output": result.content}


def qa_agent(state: State):
    """问答代理，基于知识库回答问题"""
    question = state["input"]
    context = state.get("context", "")
    result = llm.invoke(f"基于以下上下文回答问题: {context}\n\n问题: {question}")
    return {"output": result.content}


def information_extract_agent(state: State):
    """从内容中提取关键信息"""
    content = state["input"]
    result = llm.invoke(f"从以下内容中提取关键信息: {content}")
    return {"output": result.content}


def router_agent(state: State):
    """路由决策代理"""
    response = llm.invoke(
        [
            SystemMessage(
                content="""分析用户请求并分类到最合适的处理类型:
        - "search": 搜索信息、查找资料、检索内容
        - "summarize": 总结、概括、提炼要点
        - "organize": 整理、分类、组织知识结构
        - "qa": 回答问题、解释概念、提供解答
        - "extract": 提取信息、获取关键点、抽取出重要内容
        
        只回复一个词: search, summarize, organize, qa, 或 extract"""
            ),
            HumanMessage(content=state["input"]),
        ]
    )

    decision = response.content.strip().lower()

    # 决策逻辑优化
    if decision not in ["search", "summarize", "organize", "qa", "extract"]:
        # 基于关键词的默认路由
        input_lower = state["input"].lower()
        if any(
            word in input_lower for word in ["搜索", "查找", "找", "search", "find"]
        ):
            decision = "search"
        elif any(word in input_lower for word in ["总结", "概括", "summarize"]):
            decision = "summarize"
        elif any(word in input_lower for word in ["整理", "分类", "组织", "organize"]):
            decision = "organize"
        elif any(word in input_lower for word in ["提取", "抽取", "extract"]):
            decision = "extract"
        else:
            decision = "qa"  # 默认作为问答处理

    return {"decision": decision}


def route_decision(state: State):
    """路由决策"""
    return state["decision"]


# 构建工作流
router_builder = StateGraph(State)

# 添加节点
router_builder.add_node("router", router_agent)
router_builder.add_node("search", knowledge_search_agent)
router_builder.add_node("summarize", content_summarize_agent)
router_builder.add_node("organize", knowledge_organize_agent)
router_builder.add_node("qa", qa_agent)
router_builder.add_node("extract", information_extract_agent)

# 构建路由
router_builder.add_edge(START, "router")
router_builder.add_conditional_edges(
    "router",
    route_decision,
    {
        "search": "search",
        "summarize": "summarize",
        "organize": "organize",
        "qa": "qa",
        "extract": "extract",
    },
)

# 所有处理节点连接到END
router_builder.add_edge("search", END)
router_builder.add_edge("summarize", END)
router_builder.add_edge("organize", END)
router_builder.add_edge("qa", END)
router_builder.add_edge("extract", END)

# 编译工作流
knowledge_workflow = router_builder.compile()

# # Invoke
# state = knowledge_workflow.invoke({"input": "帮我整理项目管理相关的知识"})
# print(state["output"])
