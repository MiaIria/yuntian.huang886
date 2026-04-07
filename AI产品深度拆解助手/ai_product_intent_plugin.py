import re

def handler(args):
    """
    Coze 插件入口函数 (如果代码框默认是 def main(args): 请改成 main)
    作用：判断用户的输入是网址，还是普通的产品名称。
    """
    # 安全提取 query 参数
    # 在 Coze Code 节点中，输入参数通常保存在 args.input 字典里
    # 如果是早期的 Plugin 格式，可能是直接作为一个字典传入
    query = ""
    try:
        if isinstance(args, dict) and "query" in args:
            query = args.get("query")
        elif hasattr(args, 'input'):
            input_val = args.input
            if isinstance(input_val, dict) and "query" in input_val:
                query = input_val.get("query")
            elif hasattr(input_val, 'query'):
                query = input_val.query
            elif hasattr(input_val, 'get'):
                query = input_val.get("query", "")
    except Exception:
        pass

    query = str(query).strip()

    # 简单的 URL 匹配正则
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    
    match = url_pattern.search(query)
    
    if match:
        extracted_url = match.group(0)
        return {
            "is_url": True,
            "extracted_url": extracted_url,
            "product_name": ""
        }
    else:
        return {
            "is_url": False,
            "extracted_url": "",
            "product_name": query
        }
