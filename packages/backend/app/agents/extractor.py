import json
import re
from typing import Any
from app.agents.method import fix_json_format
from langchain_core.messages import AIMessage

class ResponseExtractor:
    
    @staticmethod
    def extract_response(response: dict) :
        """从响应中提取文本内容"""
        data = None
        if "messages" in response:
            if isinstance(response["messages"][-1], AIMessage):
                data = response["messages"][-1].content
            else:
                for msg in response["messages"]:
                    if isinstance(msg, AIMessage):
                        data = msg.content
                        break
        return data
    
    @staticmethod
    def extract_json(response: Any):
        """从响应中提取 JSON（处理 markdown 代码块）"""
        text = ResponseExtractor.extract_response(response)
        
        if not text:
            return {}
        json_pattern = r'```json\s*(.*?)\s*```'
        match = re.search(json_pattern, text, re.DOTALL)
        if match:
            text = match.group(1).strip()
        print(text)
        try:
            return json.loads(text)
        except json.JSONDecodeError :
            text = fix_json_format(text)
            try:
                return json.loads(text)
            except json.JSONDecodeError as e:
                return {"error": f"JSON decode error: {str(e)}"}
    
    @staticmethod
    def extract_reasoning(response: Any):
        """从响应中提取 reasoning"""
        reasoning = None
        messages = response.get("messages", [])
        for msg in messages:
            if isinstance(msg, AIMessage) and hasattr(msg, "additional_kwargs") and "reasoning_content" in msg.additional_kwargs:
                reasoning = msg.additional_kwargs["reasoning_content"]
                break
        return reasoning
    
    @staticmethod
    def extract_list(response: Any):
        """从响应中提取列表"""
        try:
            return ResponseExtractor.extract_json(response)
        except json.JSONDecodeError:
            return []