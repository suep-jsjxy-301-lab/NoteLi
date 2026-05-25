import re

@staticmethod
def escape_quotes_in_strings(json_str: str) -> str:
    """转义 JSON 字符串值中的引号"""
    result = []
    i = 0
    in_string = False

    while i < len(json_str):
        char = json_str[i]
        if char == '"' and (i == 0 or json_str[i-1] != '\\'):
            if in_string:
                # 检查是否是字符串结束（后面是 : , } ] 或空白后跟这些字符）
                remaining = json_str[i+1:].lstrip()
                if remaining and remaining[0] in ':,}]':
                    in_string = False
                    result.append(char)
                else:
                    # 字符串内的引号，转义
                    result.append('\\"')
            else:
                in_string = True
                result.append(char)
        else:
            result.append(char)
        i += 1
    
    return ''.join(result)

@staticmethod
def fix_json_format(json_str: str) -> str:
    """修复 JSON 格式问题：转义引号、给属性名加引号等"""
    
    # 1. 先转义字符串内的引号
    json_str = escape_quotes_in_strings(json_str)
    
    # 2. 给没有引号的属性名添加双引号
    # 匹配类似 key: value 的格式（key 没有引号）
    json_str = re.sub(r'([{,])\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', json_str)
    
    # 3. 处理单引号的属性名或值
    json_str = re.sub(r"'([^']*)'", r'"\1"', json_str)
    
    return json_str