from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from knowledge.loader import load_documents
from knowledge.splitter import split_documents
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "storage/faiss_index"

def get_embeddings():

    return OpenAIEmbeddings(
        api_key=os.getenv("SILICONFLOW_API_KEY"),
        base_url="https://api.siliconflow.cn/v1",
        model="BAAI/bge-large-zh-v1.5"
    )

def create_vector_db():

    documents = load_documents()
    print(f"load_documents返回 {len(documents)} 个文档")

    chunks = split_documents(documents)
    print(f"split_documents返回 {len(chunks)} 个chunks")

    embeddings = get_embeddings()

    if not os.path.exists(DB_PATH):
        os.makedirs(DB_PATH)

    db = FAISS.from_documents(chunks, embeddings)

    db.save_local(DB_PATH)

    return db

def load_vector_db():

    embeddings = get_embeddings()

    db = FAISS.load_local(
        DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return db

def get_vector_db():

    index_file = os.path.join(DB_PATH, "index.faiss")
    if os.path.exists(index_file):

        print("加载已有向量数据库...")

        return load_vector_db()

    else:

        print("创建新的向量数据库...")

        return create_vector_db()