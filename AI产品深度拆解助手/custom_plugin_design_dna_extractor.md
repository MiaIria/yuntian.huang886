# 自定义插件设计：AI 产品 DNA 提取器 (AI Product DNA Extractor)

为了提升“AI 产品深度拆解助手”分析的深度，我们为你设计了一个可以自主编写 Python 代码实现的自定义插件。

## 1. 插件目标
通过爬取目标产品的官网 HTML，提取隐藏在代码中的“基因”信息（如 SEO 元数据、社交账号、底层技术栈迹象），为后续的 AI 分析提供结构化数据支撑。

## 2. 核心架构
- **输入**: `url` (String)
- **输出**: `product_dna` (JSON Object)

## 3. 开发思路与逻辑步骤

### 第一步：环境准备
你需要准备 `httpx` (或 `requests`) 用于网络请求，`beautifulsoup4` 用于解析 HTML。

### 第二步：数据抓取 (Scraping)
- 设置自定义 `User-Agent`，模拟浏览器访问以规避基础反爬。
- 获取网页的完整 HTML 源代码。

### 第三步：元数据提取 (Metadata Extraction)
- **SEO 信息**: 提取 `<title>`、`<meta name="description">`、`<meta name="keywords">`。
- **社交链接**: 查找包含 `github.com`、`twitter.com`、`discord.gg`、`producthunt.com` 的 `<a>` 标签。

### 第四步：技术栈探测 (Tech Detection)
- **关键词扫描**: 在 HTML 中搜索以下关键词的频率或存在性：
    - 前端: `Next.js`, `Vercel`, `Tailwind`
    - AI 相关: `OpenAI`, `GPT`, `Claude`, `Anthropic`, `LangChain`, `LlamaIndex`
    - 其他: `Analytics`, `Stripe` (支付)

### 第五步：结果封装 (JSON Package)
将提取到的信息整理成如下 JSON 结构：
```json
{
  "seo": { "title": "...", "description": "..." },
  "social_links": ["https://github.com/...", "https://twitter.com/..."],
  "tech_indicators": ["Next.js", "OpenAI"],
  "raw_keywords": "..."
}
```

## 4. 在 Coze 中实现的建议
- 建议使用 Coze 的 **Code 节点** (支持 Python 3.10) 进行开发。
- 将此插件作为工作流中的第一步，它的输出将直接喂给大模型分析节点。

---

**待命状态**: 当你准备好开始编写 Python 代码时，请告诉我，我将为你提供完整的代码实现！
