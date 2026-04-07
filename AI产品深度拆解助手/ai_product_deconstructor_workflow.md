# AI 产品深度拆解助手：可视化工作流设计

为了让你更清晰地理解整个智体的运行逻辑，我为你设计了如下流程图。你可以直接参考这个结构在 Coze 的 `Workflow` 页面进行搭建。

```mermaid
graph TD
    %% 节点定义
    Start((开始节点))
    Intent[意图识别/分类 Node]
    IsURL{输入类型识别}
    DNA_Plugin[插件：DNA提取器<br/>Python自定义]
    LinkReader[插件：Link Reader]
    SearchPlugin[插件：Google Search]
    LLM_Analysis[LLM分析节点<br/>PM拆解框架]
    End((结束节点))

    %% 流程连接
    Start --> Intent
    Intent --> IsURL
    
    %% 分支：URL 路径
    IsURL -- 是URL --> DNA_Plugin
    DNA_Plugin --> LinkReader
    LinkReader --> LLM_Analysis
    
    %% 分支：产品名称路径
    IsURL -- 是产品名 --> SearchPlugin
    SearchPlugin --> LLM_Analysis
    
    %% 汇总输出
    LLM_Analysis --> End

    %% 样式美化
    style DNA_Plugin fill:#f9f,stroke:#333,stroke-width:2px
    style LLM_Analysis fill:#bbf,stroke:#333,stroke-width:2px
    style IsURL fill:#fff4dd,stroke:#d4a017,stroke-width:2px
```

## 流程节点详解

1. **开始节点 (Start)**: 接收用户输入的 `product_query` (网址或名称)。
2. **意图识别 (Intent)**: 这是一个简单的 LLM 节点，用于判断输入是 `URL` 还是 `Product Name`。
3. **选择器 (Selector)**: 根据意图识别的结果，走不同的分支。
4. **DNA 提取器 (DNA Extractor)**: **这就是我们要用 Python 自主开发的插件**。它负责抓取网页源码，提取 SEO、社交链接和技术栈等“底层基因”。
5. **Link Reader**: 辅助读取网页的具体正文文案，补充 DNA 提取器无法覆盖的描述信息。
6. **Google Search**: 如果用户只输入了名称，则通过搜索获取相关背景。
7. **LLM 分析 (Analysis)**: 这是最核心的“大脑”节点，汇总所有原始数据，套用 PM 分析框架进行深度拆解。
8. **结束节点 (End)**: 将分析结果以精美的 Markdown 报告形式返回给用户。
