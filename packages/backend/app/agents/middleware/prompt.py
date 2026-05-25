from langchain.messages import SystemMessage
from langchain.agents.middleware import dynamic_prompt, ModelRequest

@dynamic_prompt
def get_dynamic_prompt(request: ModelRequest) -> str:
    """根据当前状态动态生成提示词"""
    taskstep = request.runtime.context.get("step", None)  # 获取当前步骤
    task = taskstep.name
    description = taskstep.description
    system_msg=f"""
你是一个笔记管理系统的智能助手,
你的功能有["problem analysis","create note","update note","create category","update category","delete note","delete category","summarize work"],
当前你的任务是{task},
当前任务的详细描述:
{description},
不要生成解释性文字和思考过程,只需要根据描述完成任务,并且严格按照描述中的格式回复结果,不要回复其他文字

"""
    return system_msg