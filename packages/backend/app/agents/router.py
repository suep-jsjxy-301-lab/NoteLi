# app/agents/router.py
from langchain.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from app.agents.State import WorkState, Taskstep
from app.agents.base import agent,chat_agent
from app.agents.extractor import ResponseExtractor
from langgraph.types import Command

async def start_node(state: WorkState) :
    response = await chat_agent.ainvoke(input={"messages":HumanMessage(state["context"])})
    data = ResponseExtractor.extract_response(response)
    if data == "question":
        return Command(goto="question")
    state["output"] = data
    return Command(goto=END,update={"output": data})

async def question_node(state: WorkState) :
    name = ["create note","update note","delete note","search notes","create category","update category","delete category","search categories","done"]
    task = Taskstep(name="problem analysis", description=f"""
用户输入的问题是：{state['context']},
请帮我分析这个问题,并拆分成具体的步骤,最后一个步骤为done,表示任务完成,只需要分析问题，不需要执行任务,
回复的格式是json,只包含一个steps字段,steps是一个数组,每个元素包含name,description两个字段,
name只能从{name}里选择,不能选择没有出现过的name,
description只包含步骤需要的参数和回复格式,不需要包含其他内容,步骤参数和回复格式的描述需要足够详细以确保后续步骤能够正确执行,
以下是步骤功能的描述:
"create note"不要填写参数信息,新建的笔记默认属于用户的默认分类，标题和内容为空，标签为空，未加星标,回复格式为json,包含一个notes字段,notes是一个列表,为context中的notes,
"update note"需要参数:note_id, title, content, category_id, tags, starred,回复格式为json,包含一个notes字段,notes是一个列表,为context中的notes,
"delete note"需要参数:note_id,回复格式为json,包含一个notes字段,notes是一个列表,为context中的notes,
"search notes"不需要参数,回复格式是json,包含一个notes字段,notes是一个列表,为context中的notes,
"create category"需要参数:category_id, category_name,回复格式为json,包含一个categories字段,categories是一个列表,为context中的categories,
"update category"需要参数:id, category_id, category_name,回复格式为json,包含一个categories字段,categories是一个列表,为context中的categories,
"delete category"需要参数:id,回复格式为json,包含一个categories字段,categories是一个列表,为context中的categories,
"search categories"不需要参数,回复格式为json,包含一个categories字段,categories是一个列表,为context中的categories,
""")
    return {"steps" : [task]}

async def router_node(state: WorkState) :
    pass

async def problem_analysis_node(state: WorkState) :
    agent_context = {"user_id" : state["user_id"], "step": state["steps"].pop(0)}
    response = await agent.ainvoke(context=agent_context, input={"messages": [HumanMessage(content="请按照提示词完成问题分析,不要执行其他任务")]})
    #reasoning = ResponseExtractor.extract_reasoning(response)
    print(response)
    data = ResponseExtractor.extract_json(response)
    print(data)
    steps =[]
    for step in data["steps"] :
        task = Taskstep(name=step["name"], description=step["description"])
        steps.append(task)
    return {"steps" : steps,"work": steps.copy()}
    
async def create_note_node(state: WorkState) :
    agent_context = {
        "user_id" : state["user_id"], 
        "step": state["steps"].pop(0),
        "notes": state["notes"],
        "categories" : state["categories"],
    }
    response = await agent.ainvoke(context=agent_context, input={"messages": [HumanMessage(content="请按照提示词完成创建笔记,不要执行其他任务")]})
    print(response)
    notes = ResponseExtractor.extract_json(response)
    if isinstance(notes, list) :
        return {"notes" : notes}
    return {"notes" : [notes]}

async def update_note_node(state: WorkState) :
    agent_context = {
        "user_id" : state["user_id"], 
        "step": state["steps"].pop(0),
        "notes": state["notes"],
        "categories" : state["categories"],
    }
    print("notes")
    print(state["notes"])
    response = await agent.ainvoke(context=agent_context, input={"messages": [HumanMessage(content="请按照提示词完成修改笔记,不要执行其他任务")]})
    print(response)
    notes = ResponseExtractor.extract_json(response)
    if isinstance(notes, list) :
        return {"notes" : notes}
    return {"notes" : [notes]}

async def delete_note_node(state: WorkState) :
    agent_context = {
        "user_id" : state["user_id"], 
        "step": state["steps"].pop(0),
        "notes": state["notes"],
        "categories" : state["categories"],
    }
    response = await agent.ainvoke(context=agent_context, input={"messages": [HumanMessage(content="请按照提示词完成删除笔记,不要执行其他任务")]})
    print(response)

async def search_notes_node(state: WorkState) :
    agent_context = {
        "user_id" : state["user_id"],
        "step" : state["steps"].pop(0)
    }
    response = await agent.ainvoke(context=agent_context,input={"messages": [HumanMessage(content="请按照提示词完成搜索笔记,不要执行其他任务")]})
    notes = ResponseExtractor.extract_json(response)
    if isinstance(notes, list) :
        return {"notes" : notes}
    return {"notes" : [notes]}

async def create_category_node(state: WorkState) :
    agent_context={
        "user_id" : state["user_id"], 
        "step": state["steps"].pop(0),
        "notes": state["notes"],
        "categories" : state["categories"],
    }
    response = await agent.ainvoke(context=agent_context, input={"messages": [HumanMessage(content="请按照提示词完成创建分类,不要执行其他任务")]})
    print(response)
    categories = ResponseExtractor.extract_json(response)
    if isinstance(categories, list):
        return {"categories" : categories}
    return {"categories" : [categories]}
    
async def update_category_node(state: WorkState) :
    agent_context={
        "user_id" : state["user_id"], 
        "step": state["steps"].pop(0),
        "notes": state["notes"],
        "categories" : state["categories"],
    }
    response = await agent.ainvoke(context=agent_context, input={"messages": [HumanMessage(content="请按照提示词完成修改分类,不要执行其他任务")]})
    print(response)
    categories = ResponseExtractor.extract_json(response)
    if isinstance(categories, list):
        return {"categories" : categories}
    return {"categories" : [categories]}
    
async def delete_category_node(state: WorkState) :
    agent_context={
        "user_id" : state["user_id"], 
        "step": state["steps"].pop(0),
        "notes": state["notes"],
        "categories" : state["categories"],
    }
    response = await agent.ainvoke(context=agent_context, input={"messages": [HumanMessage(content="请按照提示词完成删除分类,不要执行其他任务")]})
    print(response)
    return {"categories" : ResponseExtractor.extract_json(response)}

async def search_categories_node(state: WorkState) :
    agent_context={
        "user_id" : state["user_id"], 
        "step": state["steps"].pop(0),
        "notes": state["notes"],
        "categories" : state["categories"],
    }
    response = await agent.ainvoke(context=agent_context, input={"messages": [HumanMessage(content="请按照提示词完成搜索分类,不要执行其他任务")]})
    print(response)
    categories = ResponseExtractor.extract_json(response)
    if isinstance(categories, list):
        return {"categories" : categories}
    return {"categories" : [categories]}

async def done_node(state: WorkState) :
    task = Taskstep(
        name="summarize work", 
        description=f"""
    请总结一下你完成的工作,并用一句话概括这个工作的结果,回复的格式是json,包含一个summary字段,summary是对这个工作的总结,尽量精简:
    用户的问题是：{state['context']},
    你完成的工作是：{state['work']}
    """)
    agent_context = {
        "user_id" : state["user_id"],
        "step": task,
    }
    response = await agent.ainvoke(context=agent_context, input={"messages": [HumanMessage(content="请按照提示词完成工作总结,不要执行其他任务")]})
    print(response)
    return {"output" : ResponseExtractor.extract_json(response).get("summary", "")}

def route_decision(state: WorkState) :
    """根据当前状态进行路由决策"""
    return state["steps"][0].name

router_builder = StateGraph(WorkState)

router_builder.add_node("start",start_node)
router_builder.add_node("question", question_node)
router_builder.add_node("router", router_node)
router_builder.add_node("problem_analysis", problem_analysis_node)
router_builder.add_node("create_note", create_note_node)
router_builder.add_node("update_note", update_note_node)
router_builder.add_node("delete_note", delete_note_node)
router_builder.add_node("search_notes",search_notes_node)
router_builder.add_node("create_category", create_category_node)
router_builder.add_node("update_category", update_category_node)
router_builder.add_node("delete_category", delete_category_node)
router_builder.add_node("search_categories",search_categories_node)
router_builder.add_node("done", done_node)

router_builder.add_edge(START, "start")
router_builder.add_edge("question", "router")
router_builder.add_conditional_edges(
    "router",
    route_decision,
    {
        "problem analysis": "problem_analysis",
        "create note": "create_note",
        "update note": "update_note",
        "delete note": "delete_note",
        "search notes": "search_notes",
        "create category": "create_category",
        "update category": "update_category",
        "delete category": "delete_category",
        "search categories": "search_categories",
        "done" : "done",
    },
)
router_builder.add_edge("problem_analysis", "router")
router_builder.add_edge("create_note", "router")
router_builder.add_edge("update_note", "router")
router_builder.add_edge("delete_note", "router")
router_builder.add_edge("search_notes","router")
router_builder.add_edge("create_category", "router")
router_builder.add_edge("update_category", "router")
router_builder.add_edge("delete_category", "router")
router_builder.add_edge("search_categories","router")
router_builder.add_edge("done", END)

workflow = router_builder.compile()