from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
import os

def load_documents():

    documents = []

    for file in os.listdir("data"):
        path = f"data/{file}"

        if file.endswith(".pdf"):
            loader = PyPDFLoader(path)
            docs = loader.load()
            documents.extend(docs)

        elif file.endswith(".txt"):

            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

            documents.append(
                Document(
                    page_content=text,
                    metadata={"source": file}
                )
            )
    print("加载文档数量:", len(documents))

    return documents