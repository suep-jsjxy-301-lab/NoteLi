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

@dynamic_prompt
def get_chat_prompt(request: ModelRequest) -> str:
    """根据当前动态生成提示词"""

    system_msg=f"""
你是一个笔记管理系统的智能辅助助手,
你需要对用户的问题进行分析,
回复一个字符串,
若用户只是单纯想要聊天,则回复为对用户的回复,
若不是单纯聊天,则回复"question",不要回复其他文字,
"""
    return system_msg