# AI 产品 DNA 提取器 (DNA Extractor) 工作流设计

在拆解 AI 产品时，很多关键信息（“产品基因”）往往隐藏在网页的底层代码中，而普通的文字阅读插件只能获取表面文本。这个插件的**具体作用**就是充当“X光机”，透视产品官网，提取深层价值数据，为后端的“LLM 大脑节点”提供极高密度的结构化情报。

## 🎯 插件的具体作用与核心思路

1. **核心定位**：将一个干瘪的 `URL` 转化为一个包含 **流量特征、技术底层、社区活跃度** 等关键指标的丰富 `JSON` 数据包。
2. **SEO 提取**：抓取 `Title`, `Description`, `Keywords`。这些隐藏在 `<head>` 里的标签往往是产品经理（PM）最真实、最原始的产品定位和买点提炼（即使页面上没直接写）。
3. **技术栈扫描（Tech Detection）**：通过扫描网页正文或代码，寻找特定关键词（如是否使用了 Next.js, Vercel，底层模型是提到的 OpenAI 还是 Anthropic）。
4. **社群溯源（Social Links）**：寻找官网指向的 GitHub、Discord、Twitter 链接，这能帮助判断产品是开源向、极客圈、还是 C 端大众向。

---

## 🗺️ 插件内部工作流可视化图 (Mermaid)

下面是该插件内部代码执行的逻辑流程图：

```mermaid
graph TD
    %% 节点定义
    Input([输入参数: URL 网址])
    
    Fetch[🕷️ Http 请求与反爬<br>发送带User-Agent的请求]
    CheckStatus{HTTP状态码返回}
    
    ParseDOM[🔍 DOM 树解析<br>使用 BeautifulSoup4 解析 HTML]
    Error[⚠️ 返回错误或空数据]
    
    subgraph 核心提取引擎 (Extraction Engine)
        SEO[📊 SEO 信息提取<br>Title / Description / Meta Keywords]
        Social[🔗 社群链接探测<br>寻找匹配 GitHub/Twitter/Discord 的 a 标签]
        Tech[🛠️ 技术特征扫描<br>正则匹配页面内的技术关键词]
    end
    
    Package[📦 JSON 封装与格式化]
    Output([输出参数: product_dna 结构化数据])

    %% 流程连接
    Input --> Fetch
    Fetch --> CheckStatus
    CheckStatus -- 200 OK --> ParseDOM
    CheckStatus -- 非 200 (如 403 / 404) --> Error
    
    ParseDOM --> SEO
    ParseDOM --> Social
    ParseDOM --> Tech
    
    SEO --> Package
    Social --> Package
    Tech --> Package
    
    Package --> Output
    Error --> Output
    
    %% 样式美化
    style Input fill:#e1f5fe,stroke:#0288d1,stroke-width:2px
    style Output fill:#e8f5e9,stroke:#388e3c,stroke-width:2px
    style Fetch fill:#fff3e0,stroke:#f57c00
    style ParseDOM fill:#f3e5f5,stroke:#8e24aa
```

## ⚙️ 输入与输出设计

### 📥 输入参数 (Input)
*   **参数名**: `url`  (String) - 需要解剖的 AI 产品官网地址。

### 📤 输出参数 (Output)
考虑到 Coze 的返回值最好是清晰的字典类型，最终输出（Output）结构如下：
*   **`seo_info`** (String): 包含抓取到的 Title 和 Description 的组合文本。
*   **`social_links`** (String): 返回逗号分隔的社交平台链接。
*   **`tech_stack`** (String): 探测到的相关技术名词汇编。
