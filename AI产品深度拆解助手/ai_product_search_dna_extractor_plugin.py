def handler(args):
    """
    Coze 自定义代码节点入口：全网搜索 DNA 提取器
    入参定义要求: product_name (String)
    出参定义要求: 
        - official_positioning (String)
        - market_competitors (String)
        - funding_and_team (String)
        - public_sentiment (String)
    """
    # 依赖：需在 Coze 平台左侧 "依赖包" 中搜索并安装 duckduckgo-search
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        return {
            "official_positioning": "依赖导入失败，请在 Coze 依赖库中添加 duckduckgo-search",
            "market_competitors": "失败",
            "funding_and_team": "失败",
            "public_sentiment": "失败"
        }

    # 1. 安全兼容多种 Coze 传参格式
    product_name = ""
    try:
        if isinstance(args, dict) and "product_name" in args:
            product_name = args.get("product_name")
        elif hasattr(args, 'input'):
            input_val = args.input
            if isinstance(input_val, dict) and "product_name" in input_val:
                product_name = input_val.get("product_name")
            elif hasattr(input_val, 'product_name'):
                product_name = input_val.product_name
            elif hasattr(input_val, 'get'):
                product_name = input_val.get("product_name", "")
    except Exception:
        pass
        
    product_name = str(product_name).strip()
    if not product_name:
        return {
            "official_positioning": "未检测到有效的产品名称输入。请确保输入了正常的文本。",
            "market_competitors": "无",
            "funding_and_team": "无",
            "public_sentiment": "无"
        }

    # 2. 定向检索引擎初始化
    ddgs = DDGS()
    
    # 内部隐形构造出四个不同维度的搜索 Query
    queries = {
        "official_positioning": f'"{product_name}" AI product official features overview',
        "market_competitors": f'"{product_name}" alternatives vs competitors',
        "funding_and_team": f'"{product_name}" startup founder funding valuation',
        "public_sentiment": f'"{product_name}" review reddit feedback issues pros cons'
    }
    
    results = {
        "official_positioning": [],
        "market_competitors": [],
        "funding_and_team": [],
        "public_sentiment": []
    }

    # 3. 逐个进行定向检索，提取浓缩 Snippet 摘要
    def search_and_extract(search_text):
        try:
            # 限制每个维度只取前 3 条核心结果，避免 Coze 节点耗时超限
            raw_results = list(ddgs.text(search_text, max_results=3))
            snippets = []
            for item in raw_results:
                if 'body' in item:
                    snippets.append(item['body'])
            return " | ".join(snippets) if snippets else "未检索到明显数据"
        except Exception as e:
            return f"检索中断: {str(e)}"

    # 顺序执行（若要追求极限速度可用 ThreadPoolExecutor 并发，但 Coze 运行沙箱对多线程支持各异，串行更稳）
    for key, q_text in queries.items():
        results[key] = search_and_extract(q_text)

    # 4. JSON 组装与返回给大模型引擎
    return {
        "official_positioning": results["official_positioning"],
        "market_competitors": results["market_competitors"],
        "funding_and_team": results["funding_and_team"],
        "public_sentiment": results["public_sentiment"],
    }
