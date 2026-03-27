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

    docs = db.similarity_search(query, k=15)

    filter_map = {
        "criminal": "IPC",
        "cyber": "IT Act",
        "constitutional": "Constitution"
    }
    docs = rerank_docs(query, docs)

    law_filter = filter_map.get(intent)

    if law_filter:
        filtered = [
            d for d in docs
            if law_filter.lower() in d.metadata.get("law", "").lower()
        ]

        if filtered:
            docs = filtered

    return docs

def enhance_query(query):
    query = query.lower()

    if "kill" in query:
        return query + " murder IPC section 302"

    if "hack" in query:
        return query + " cyber crime IT Act"

    return query

def rerank_docs(query, docs):
    query_words = set(query.lower().split())

    scored_docs = []

    for d in docs:
        text = (d.page_content + str(d.metadata)).lower()

        score = sum(1 for word in query_words if word in text)

        scored_docs.append((score, d))

    scored_docs.sort(key=lambda x: x[0], reverse=True)

    return [d for _, d in scored_docs[:5]]