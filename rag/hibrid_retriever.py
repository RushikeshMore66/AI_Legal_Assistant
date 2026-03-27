from langchain.vectorstores import FAISS
from rag.embeddings import get_embeddings
from rank_bm25 import BM25Okapi


def get_db():
    return FAISS.load_local(
        "db",
        get_embeddings(),
        allow_dangerous_deserialization=True
    )