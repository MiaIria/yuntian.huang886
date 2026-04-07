"""
意图分类插件 - Intent Classification Plugin for Coze (新版 SDK 适配)
用于分类用户问题的两个场景：打招呼寒暄、其他
"""

from runtime import Args
from typings.classify_intent.classify_intent import Input, Output
from enum import Enum


class IntentType(Enum):
    """意图类型枚举"""
    GREETING = "greeting"           # 打招呼寒暄类
    OTHER = "other"                 # 其他类


# 打招呼寒暄关键词（详尽版）
GREETING_KEYWORDS = [
    # 问候类
    "你好", "您好", "嗨", "嗨你好", "你好呀", "哈喽", "hello", "hi",
    # 身份询问类
    "你是谁", "你是", "你是干什么的", "你叫什么", "你是什么",
    # 技能询问类
    "你有什么技能", "你会什么", "你能做什么", "你有哪些功能", "你能干什么",
    # 介绍类
    "介绍一下", "介绍下自己", "说说你自己", "自我介绍一下",
    # 寒暄类
    "早上好", "下午好", "晚上好", "很高兴认识你", "认识你很高兴",
]


def classify_intent(user_input: str) -> dict:
    """分类用户输入的意图"""
    if not user_input or not user_input.strip():
        return {
            "type": IntentType.OTHER.value,
            "need_rag": True
        }

    # 统一转小写进行匹配
    text = user_input.lower().strip()

    # 1. 检查是否匹配打招呼寒暄
    for keyword in GREETING_KEYWORDS:
        if keyword in text:
            return {
                "type": IntentType.GREETING.value,
                "need_rag": False
            }

    # 2. 默认归类为其他，需要知识库检索
    return {
        "type": IntentType.OTHER.value,
        "need_rag": True
    }


import random


def get_response_by_intent(intent: str) -> str:
    """根据意图返回相应的回答"""
    if intent == IntentType.GREETING.value:
        # 定义三个版本的回复语
        responses = [
            # 版本 1：专业沉稳型
            "您好！我是 yuntian.huang 的专属 AI 助理。无论是了解他的教育背景、项目经验、技术见解，还是探讨行业趋势、职业规划、生活感悟，我都能为您提供有价值的信息与陪伴。请问今天想聊些什么？",

            # 版本 2：优雅睿智型
            "您好！欢迎来到 yuntian.huang 的智能助手空间。在这里，您可以探寻他的成长轨迹与专业见解，也可以就任何话题展开深入交流。让我们的对话既有深度，也兼备广度。期待与您畅聊！",

            # 版本 3：自信从容型
            "您好！我是 yuntian.huang 的专属 AI 助理，关于他的一切，我都能为您详细解答；若您想聊聊其他话题，我也同样乐意奉陪。无论何种需求，都请您尽管开口，我随时为您服务。"
        ]
        # 随机选择一个版本返回
        return random.choice(responses)
    else:
        return "我理解您的问题，让我为您查找 yuntian.huang 的相关背景信息..."


def handler(args: Args[Input]) -> Output:
    """
    Coze 插件入口函数 (新版 SDK)
    """
    # 1. 获取输入
    user_text = args.input.user_input

    # 2. 分类意图
    classification = classify_intent(user_text)

    # 3. 生成回复
    response = get_response_by_intent(classification["type"])

    # 4. 返回完整字典（需匹配元数据定义）
    return {
        "user_input": user_text,
        "type": classification["type"],
        "need_rag": classification["need_rag"],
        "response": response
    }
