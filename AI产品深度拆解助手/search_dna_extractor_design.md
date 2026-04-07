# 全网搜索 DNA 提取器 (Search DNA Extractor) 插件设计思

## 1. 核心痛点与定位
在使用系统自带的 `Google Search` 插件时，往往只会返回一堆零散的、字数受限的网页 Snippets（摘要），大模型直接消化这些碎片的效率极低，且容易遗漏核心商业信息。
**本插件的定位**：充当一个自动化的“商业调查员”。当用户只输入某个产品名称（如 "Sora" 或 "Kimi"）时，它在后台**自动模拟多维度搜索**，对返回的搜索内容进行二次清洗、去重和重组，直接向大模型吐出精准的结构化基因（DNA）数据。

---

## 2. 插件的输入与输出设计

### 📥 核心输入 (Input)
*   **`product_name`** (String): 也就是前置意图识别节点判断出来的非 URL 文本。

### 📤 核心输出 (Output)
提取出的结构化情报（向后续大模型节点提供可以直接套用分析框架的原料）：
*   **`official_positioning`** (String): 提取到的官方或维基百科口吻的产品定位与功能概述。
*   **`market_competitors`** (String): 在搜索结果中常与该产品一起被提及的竞品名单（如搜索 Kimi 常带出 月之暗面、智谱、Claude 等）。
*   **`funding_and_team`** (String): 捕捉到的融资背景、背后大厂、创始人信息（AI 领域极度看重产品背后的算力和资本支撑）。
*   **`public_sentiment`** (String): 综合的外界声量关键词（如“免费、长文本牛逼、总是崩溃、代码能力强”等）。

---

## 3. 内部执行逻辑流 (Workflow / Code Logic)

在这个 Python 插件内部，我们不能只做一次单一的搜索，而是要**隐性地进行多次定向搜索并熔炼数据**。

```mermaid
graph TD
    Input([Input: product_name])
    
    subgraph 多核并发检索引擎
        Q1[搜索动作 1: <br> '{product_name} 官网 功能 介绍']
        Q2[搜索动作 2: <br> '{product_name} 创始人 融资 背后公司']
        Q3[搜索动作 3: <br> '{product_name} 评测 缺点 替代品 对标']
    end
    
    Clean[数据清洗与清洗节点<br>去除无用标点代码，合并三路搜索Snippet]
    
    subgraph 关键词与实体正则提取 (DNA 提炼)
        E1[提取产品百科摘要]
        E2[提取资金/大厂背景]
        E3[提取竞品关联词]
    end
    
    Output([Output: 结构化 JSON 字段返回给你工作流的大模型])
    
    Input --> Q1 & Q2 & Q3
    Q1 & Q2 & Q3 --> Clean
    Clean --> E1 & E2 & E3
    E1 --> Output
    E2 --> Output
    E3 --> Output
```

---

## 4. 技术实现难点与方案探讨

在 Coze 中自主开发搜索插件，最大的限制是**如何稳定调用搜索引擎**而不用我们自己花钱买昂贵的 Google/Bing API。
**这里有三个落地方案：**

1. **方案 A (白嫖第三方免费库)**：使用 Python 的开源搜索轮子，如 `duckduckgo-search`。这个库在 Coze 沙箱里 `pip install duckduckgo-search` 后通常可以直接发出请求，不需要 API Key，极其适合做低成本检索。
2. **方案 B (对接原生搜索 API)**：利用诸如 `SerpApi` / `Tavily` 这样的专为 LLM 设计的搜索接口。优点是格式极度对口，结构化好，但缺点是免费额度有限。
3. **方案 C (Coze 原生联动)**：跳过写 Python 的纯自研，在你的 Coze 工作流中，将【产品名称】直接以批量运行（Batch）的方式，分别喂给 3 个 Coze 系统自带的 `Google Search` 插件（搜索词用大模型拼接好），然后由一个中间的 LLM 节点进行整理，不写代码。

## 5. 建议路径
如果你希望极致的可控性，并且咱们已经在 Python 插件开发上跑通了一遍，我非常建议用 **方案 A (Python + DuckDuckGo)** 来写代码实现！它能够最完美地取代你目前的纯净版 Google Search，做成完全符合 `ai_product_dna_extractor` 输入输出规范的孪生兄弟版——**`ai_product_search_dna_extractor`**！
