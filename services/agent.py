from tools.emergency_tool import is_emergency
from tools.symptom_tool import analyze_symptom
from services.medical_service import medical_chat
from utils.logger import get_logger
from core.rewrite import rewrite_query

logger = get_logger("agent")

def is_medical(text):

    text = text.lower()

    medical_keywords = [
        # 症状
        "头痛","头晕","发烧","咳嗽","腹痛","胸痛","恶心","呕吐","乏力",
        "呼吸困难","流鼻涕","喉咙痛","心慌","失眠","出汗",

        # 疾病
        "糖尿病","高血压","高血脂","感冒","肺炎","胃炎","癌","肿瘤",

        # 医疗行为
        "吃什么","能吃吗","怎么治","怎么办","怎么缓解",
        "用药","吃药","副作用","检查","诊断","治疗",

        # 药物相关
        "药","药物","降压药","抗生素","止痛药",

        # 身体状态
        "不舒服","难受","疼","症状","病","疾病"
    ]

    # 命中关键词
    for k in medical_keywords:
        if k in text:
            return True

    return False

def is_non_medical(text):

    non_medical_keywords = [
        "做饭","红烧肉","炒菜","电影","游戏",
        "编程","代码","Python","作业","考试"
    ]

    return any(k in text for k in non_medical_keywords)

def is_medical_query(text):

    if is_non_medical(text):
        return False

    return is_medical(text)

def is_symptom_question(text):
    keywords = ["痛", "难受", "不舒服", "发烧", "头晕", "咳嗽"]
    return any(k in text for k in keywords)


def medical_agent(question, history):

    logger.info("用户问题: %s", question)
    rewritten = rewrite_query(question, history)

    if not is_medical_query(rewritten):
        logger.info("识别为非医疗问题")
        return "这个问题不属于医疗咨询范围，请提问健康相关问题 😊", []

    if is_emergency(question):
        logger.warning("高风险症状触发")
        return "⚠️ 检测到高风险症状，请立即就医！", []

    if is_symptom_question(question):

        symptom = analyze_symptom(question)
    else:
        symptom = ""

    if is_symptom_question(question):
        symptom = analyze_symptom(question)
    else:
        symptom = ""

    answer, sources = medical_chat(question, history)

    if symptom:
        final_answer = f"""
    可能原因：
    {symptom}
    
    医学建议：
    {answer}
    
本回答仅供参考，请咨询专业医生。
"""
    else:
        final_answer = f"""
    💊 医学建议：
    {answer}
    
    本回答仅供参考，请咨询专业医生。
    """

    logger.info("回答完成")

    return final_answer, sources