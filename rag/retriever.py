from langchain_community.vectorstores import FAISS
from rag.embedding import get_embeddings

def get_retriever():
    return FAISS.load_local(
        "db",
        get_embeddings(),
        allow_dangerous_deserialization=True
    )

def retrieve_docs(query, intent):
    db = get_retriever()

    filter_map = {
        "criminal": "IPC",
        "cyber": "IT Act",
        "constitutional": "Constitution"
    }

    law_filter = filter_map.get(intent)

    docs = db.similarity_search(query, k=10)

    if law_filter:
        filtered = [
            d for d in docs
            if law_filter.lower() in d.metadata.get("law", "").lower()
        ]
        if filtered:
            docs = filtered

    return docs[:5]