from core.llm import get_llm
from rag.retriever import retrieve_docs
from agents.intent_classifier import classify_intent
from utils.prompt import LEGAL_PROMPT


def legal_agent(query):
    llm = get_llm()

    # 🔹 Step 1: Intent detection
    intent = classify_intent(query)
    print(f"Detected intent: {intent}")

    # 🔹 Step 2: Retrieve docs
    docs = retrieve_docs(query, intent)

    # ❗ Step 3: Handle empty retrieval (VERY IMPORTANT)
    if not docs:
        return "I don't have enough legal information to answer this query accurately."

    # 🔹 Step 4: Structured context (clean format)
    context_parts = []
    for d in docs:
    context_parts.append(
        f"""
Law: {d.metadata.get('law', 'Unknown')}
Section: {d.metadata.get('section', 'Unknown')}
Title: {d.metadata.get('title', 'Unknown')}
Content: {d.page_content}
"""
    )

    context = "\n---\n".join(context_parts)

    # 🔹 Step 5: Strong grounding prompt
    prompt = f"""
{LEGAL_PROMPT}

STRICT INSTRUCTIONS:
- Answer ONLY from the provided legal context
- DO NOT make up laws or sections
- If answer is not clearly available, say:
  "I don't have enough information from the legal database."

User Query:
{query}

Detected Intent:
{intent}

Legal Context:
{context}

Your Task:
1. Identify correct law/section
2. Explain in simple language
3. Give real-world example
4. Suggest practical actions
"""
def is_relevant(query, docs):
    query_lower = query.lower()

    for d in docs:
        text = (d.page_content + str(d.metadata)).lower()
        if any(word in text for word in query_lower.split()):
            return True

    return False
    # 🔹 Step 6: LLM call
    try:
    response = llm.invoke(prompt)
    return response.content
except Exception as e:
    return f"Error generating response: {str(e)}"