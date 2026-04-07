import ssl
import urllib.request
import re

# 尝试导入 BeautifulSoup（Coze 环境通常支持 bs4，如果不支持则使用正则 Fallback）
try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

def handler(args):
    """
    Coze 插件/代码节点入口函数 (如果代码框默认是 def handler(args): 请改成 handler)
    入参定义要求: url (String)
    出参定义要求: 
        - seo_info (String)
        - social_links (String)
        - tech_stack (String)
    """
    # 1. 兼容多种 Coze 传参格式 (支持自定义对象、字典等)
    url = ""
    try:
        if isinstance(args, dict) and "url" in args:
            url = args.get("url")
        elif hasattr(args, 'input'):
            input_val = args.input
            if isinstance(input_val, dict) and "url" in input_val:
                url = input_val.get("url")
            elif hasattr(input_val, 'url'):
                url = input_val.url
            elif hasattr(input_val, 'get'):
                url = input_val.get("url", "")
    except Exception:
        pass
    url = str(url).strip()
    
    if not url or not url.startswith("http"):
        return {
            "seo_info": "未检测到有效的 HTTP(S) URL 输入。",
            "social_links": "无",
            "tech_stack": "无"
        }

    # 2. 配置请求头以防止基础的反爬机制拦截
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    }
    
    req = urllib.request.Request(url, headers=headers)
    
    # 忽略 SSL 证书报错
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    html_content = ""
    try:
        # 发送请求，超时设置 10 秒
        with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return {
            "seo_info": f"网站抓取失败: {str(e)}", 
            "social_links": "抓取失败", 
            "tech_stack": "抓取失败"
        }

    # 3. 提取变量初始化
    seo_title = ""
    seo_desc = ""
    social_links_result = []
    tech_stack_result = set()
    hrefs = []

    # 4. 优先使用 BeautifulSoup 解析 DOM 树
    if BeautifulSoup:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # SEO Title
        if soup.title and soup.title.string:
            seo_title = soup.title.string.strip()
        
        # SEO Description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            seo_desc = meta_desc.get('content').strip()
            
        # 提取页面所有超链接 (用于社群发现)
        a_tags = soup.find_all('a', href=True)
        hrefs = [a['href'] for a in a_tags]
    else:
        # --- Fallback: 纯正则解析降级方案 ---
        title_match = re.search(r'<title.*?>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
        if title_match:
            seo_title = title_match.group(1).strip()
            
        desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']\s*/?>', html_content, re.IGNORECASE)
        if desc_match:
            seo_desc = desc_match.group(1).strip()
            
        hrefs = re.findall(r'<a\s+(?:[^>]*?\s+)?href=["\'](.*?)["\']', html_content, re.IGNORECASE)

    # 封装 SEO 信息
    seo_info = f"【官网标题】: {seo_title}\n【官方描述】: {seo_desc}"

    # 5. 扫描并过滤核心社交和代码托管链接
    social_domains = ['github.com', 'twitter.com', 'x.com', 'discord.gg', 'discord.com/invite', 'producthunt.com']
    for href in hrefs:
        for domain in social_domains:
            if domain in href:
                social_links_result.append(href)
                
    social_links_result = list(set(social_links_result)) # 去重
    social_links = "\n".join(social_links_result) if social_links_result else "未发现相关社交媒体链接"

    # 6. 底层技术基座探测字典
    tech_keywords = {
        '前端生态': ['Next.js', 'Vercel', 'Tailwind', 'React', 'Vue', 'Nuxt'],
        'AI底层模型': ['OpenAI', 'GPT-4', 'GPT-3', 'Claude', 'Anthropic', 'Gemini', 'Llama', 'Mistral'],
        'AI框架工具': ['LangChain', 'LlamaIndex', 'HuggingFace'],
        '云服务/后端': ['Stripe', 'Supabase', 'Firebase', 'AWS', 'Cloudflare']
    }
    
    # 对整个 HTML 进行正则表达式扫描
    for category, keywords in tech_keywords.items():
        for kw in keywords:
            # 使用正则 \b 匹配单词边界，防止误匹配 (如包含 openai 的长单词，大小写不敏感)
            if re.search(r'\b' + re.escape(kw) + r'\b', html_content, re.IGNORECASE):
                tech_stack_result.add(kw)
                
    tech_stack = ", ".join(list(tech_stack_result)) if tech_stack_result else "未探测到明显的技术栈足迹"

    # 7. 组装终态给 Coze 的返回值
    return {
        "seo_info": seo_info,
        "social_links": social_links,
        "tech_stack": tech_stack
    }
