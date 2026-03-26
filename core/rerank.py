from llm import client
import re
from ..utils.logger import get_logger

logger = get_logger("rerank")

def rerank_documents(query, docs, top_k=3):

    doc_texts = []

    for i, doc in enumerate(docs):
        doc_texts.append(f"{i}. {doc.page_content[:200]}")

    docs_str = "\n".join(doc_texts)

    prompt = f"""
用户问题：
{query}

下面是一些医学资料片段：

{docs_str}

请选出最相关的 {top_k} 个片段编号。
只输出编号，例如：
0,3,5
"""

    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3",
        messages=[{"role": "user", "content": prompt}]
    )

    result = response.choices[0].message.content

    try:
        indexes = [int(x) for x in re.findall(r"\d+", result)]
    except Exception as e:
        logger.error("Rerank解析失败: %s", str(e))
        indexes = []

    selected_docs = [docs[i] for i in indexes if i < len(docs)]

    return selected_docs