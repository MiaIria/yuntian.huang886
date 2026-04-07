from runtime import Args
from typings.users.users import Input, Output
from enum import Enum
from dataclasses import dataclass, asdict
from typing import Optional

# === 枚举定义 ===

class Gender(Enum):
    """性别枚举"""
    MALE = "男"
    FEMALE = "女"
    OTHER = "其他"

class Goal(Enum):
    """健身目标枚举"""
    LOSE_WEIGHT = "减肥"
    MAINTAIN = "保持"
    GAIN_WEIGHT = "增重"
    SHAPE = "塑形"

class ActivityLevel(Enum):
    """活动强度枚举"""
    SEDENTARY = "久坐"
    LIGHT = "轻度"
    MODERATE = "中度"
    HIGH = "高强度"

class MealType(Enum):
    """用餐类型枚举"""
    BREAKFAST = "早餐"
    LUNCH = "午餐"
    DINNER = "晚餐"
    SNACK = "加餐"

# === 数据模型 ===

@dataclass
class UserProfile:
    """用户档案数据模型"""
    nickname: str
    gender: str
    age: int
    height: int
    current_weight: float
    target_weight: float
    goal: str
    weekly_target: float
    activity_level: str
    user_id: Optional[str] = None

    @classmethod
    def from_input(cls, input_data: Input) -> 'UserProfile':
        """从 Input 对象创建 UserProfile"""
        return cls(
            nickname=input_data.nickname,
            gender=input_data.gender,
            age=input_data.age,
            height=input_data.height,
            current_weight=input_data.current_weight,
            target_weight=input_data.target_weight,
            goal=input_data.goal,
            weekly_target=input_data.weekly_target,
            activity_level=input_data.activity_level,
            user_id=getattr(input_data, 'user_id', None)
        )

# === 核心逻辑 ===

def generate_summary(profile: UserProfile) -> str:
    """生成用户档案摘要"""
    summary = (
        f"已成功建立用户档案：\n"
        f"昵称：{profile.nickname}\n"
        f"基本信息：{profile.gender}，{profile.age}岁，身高{profile.height}cm\n"
        f"当前体重：{profile.current_weight}kg，目标体重：{profile.target_weight}kg\n"
        f"健身目标：{profile.goal}，每周目标：{profile.weekly_target}kg\n"
        f"活动强度：{profile.activity_level}\n"
        f"档案信息已同步，我可以开始为您制定个性化的健康建议了。"
    )
    return summary

# === Coze 插件入口 ===

def handler(args: Args[Input]) -> Output:
    """
    Coze 插件入口函数 (新版 SDK)
    """
    # 1. 解析输入
    try:
        profile = UserProfile.from_input(args.input)
    except AttributeError as e:
        # 容错处理：如果元数据定义与预期不符
        return {
            "success": False,
            "message": f"输入参数缺失或格式错误: {str(e)}",
            "summary": ""
        }

    # 2. 生成回复摘要
    summary = generate_summary(profile)

    # 3. 返回结果 (需匹配 Coze 平台的 Output 元数据定义)
    # 注意：Output 的具体字段需与你在 Coze 面板定义的元数据一致
    return {
        "success": True,
        "message": "档案创建成功",
        "summary": summary,
        "profile": asdict(profile)
    }
