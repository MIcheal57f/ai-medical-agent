from llm import client
from storage.embedding import create_vector_db,get_vector_db,load_vector_db
from core.rerank import rerank_documents
from rank_bm25 import BM25Okapi
import jieba
from ..utils.logger import get_logger

bm25 = None
corpus = None
tokenized_corpus = None
all_docs = None

logger = get_logger("rag")

def ask_medical_question(question,messages):

    db = get_vector_db()

    logger.info("用于检索的问题: %s", question)

    # =========================
    # 向量搜索
    # =========================

    vector_docs = db.similarity_search(question, k=5)
    logger.info("向量搜索返回: %d", len(vector_docs))

    # =========================
    # BM25
    # =========================

    global bm25, corpus, tokenized_corpus, all_docs

    if bm25 is None:
        logger.info("初始化 BM25...")

        all_docs = list(db.docstore._dict.values())[:100]

        corpus = [doc.page_content for doc in all_docs]
        tokenized_corpus = [list(jieba.cut(doc)) for doc in corpus]

        bm25 = BM25Okapi(tokenized_corpus)

        logger.info("BM25 初始化完成，文档数: %d", len(corpus))

    all_docs = list(db.docstore._dict.values())[:100]

    corpus = [doc.page_content for doc in all_docs]
    tokenized_corpus = [list(jieba.cut(doc)) for doc in corpus]

    bm25 = BM25Okapi(tokenized_corpus)

    tokenized_query = list(jieba.cut(question))
    scores = bm25.get_scores(tokenized_query)

    top_n = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:5]
    bm25_docs = [all_docs[i] for i in top_n]

    logger.info("BM25返回: %d", len(bm25_docs))

    for i in top_n[:3]:
        logger.info("BM25命中[%d]: %s", i, corpus[i][:50])


    # =========================
    # Hybrid
    # =========================

    docs = vector_docs + bm25_docs[:3]
    logger.info("Hybrid前总数: %d", len(docs))
    unique_docs = []
    seen = set()

    for doc in docs:
        content = doc.page_content
        if content not in seen:
            seen.add(content)
            unique_docs.append(doc)


    docs = unique_docs
    logger.info("Hybrid后数量: %d", len(docs))


    logger.info("进入Rerank数量: %d", len(docs))
    docs = rerank_documents(question, docs, top_k=3)
    if len(docs) == 0:
        logger.warning("Rerank为空，回退到向量结果")
        docs = vector_docs[:3]
    logger.info("Rerank后数量: %d", len(docs))

    context = ""
    sources = []

    for doc in docs:
        context += doc.page_content + "\n"
        source = doc.metadata.get("source", "未知来源")
        page = doc.metadata.get("page", None)

        if page is not None:
            sources.append(f"{source} page {page}")
        else:
            sources.append(source)

    prompt = f"""
你是一名专业医生，请根据以下医学资料回答问题。

医学资料：
{context}

问题：
{question}

回答时请：
1. 提供医学建议
2. 提醒用户咨询真实医生
3. 使用分点说明
"""
    messages_to_send = messages + [
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3",
        messages=messages_to_send
    )

    answer = response.choices[0].message.content

    return answer, sources