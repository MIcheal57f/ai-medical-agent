from llm import client
from ..utils.logger import get_logger

logger = get_logger("rewrite")

def rewrite_query(question,history):

    logger.info("原问题: %s", question)

    history_text = ""

    for msg in history[-6:]:
        if msg["role"]!="system":
            history_text += f"{msg['role']}: {msg['content']}\n"

    prompt = f"""
你是一名医学助手，请根据对话历史改写用户当前问题，使其更完整、明确，适合医学知识检索。

规则：
1 保持原问题意思
2. 如果用户问题不完整，要补充上下文（如疾病名称）
3. 不要出现“根据历史”等描述
4. 不要添加不存在的信息
5. 如果问题已经清晰，就保持原样
6. 不要使用占位符
7. 只输出改写后的问题

对话历史：
{history_text}

用户问题：
{question}
"""

    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3",
        messages=[{"role": "user", "content": prompt}]
    )

    rewritten = response.choices[0].message.content.strip()

    logger.info("改写后: %s", rewritten)

    return rewritten