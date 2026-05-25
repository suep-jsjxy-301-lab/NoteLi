from langchain_core.messages import AIMessage, HumanMessage
from app.agents.State import AgentState, ContextState
from langchain.agents.middleware import after_model, before_model

@before_model
def inject_reasoning(state: AgentState, runtime: ContextState):
    """✅ DeepSeek-V4-Flash 专用：正确回传 reasoning_content"""
    # 从上下文拿思考内容
    reasoning = runtime.context.get("reasoning_to_send")
    if not reasoning:
        return state

    messages = state["messages"]
    if not messages:
        return state

    # 🔥 关键 1：必须取【最后一条】AIMessage
    last_msg = messages[-1]
    if isinstance(last_msg, AIMessage):
        # 🔥 关键 2：必须重建消息，不能直接修改！
        new_msg = AIMessage(
            content=last_msg.content,
            reasoning_content=reasoning,  # ✅ 顶层字段
            additional_kwargs=last_msg.additional_kwargs
        )
        # 替换消息
        messages[-1] = new_msg
        state["messages"] = messages

    return state