from core.llm import get_llm
from rag.retriever import retrieve_docs
from agents.intent_classifier import classify_intent
from utils.prompt import LEGAL_PROMPT
from utils.memory import memory
from utils.case_memory import save_cases, get_user_cases

def is_relevant(query, docs):
    query_lower = query.lower()

    for d in docs:
        text = (d.page_content + str(d.metadata)).lower()
        if any(word in text for word in query_lower.split()):
            return True

    return False


def legal_agent(query):
    llm = get_llm()

    memory.add("user",query)

    conversation_context = memory.get_context()

    user_id = "default_user"

    save_cases(user_id, query)
    past_cases = get_user_cases(user_id)

    case_context = "\n".join(past_cases[-3:])

    intent = classify_intent(query)

    docs = retrieve_docs(query, intent)

    context = ""
    for d in docs:
        context += f"""
        Law: {d.metadata.get('law')}
        Section: {d.metadata.get('section')}
        Title: {d.metadata.get('title')}
        Content: {d.page_content}
        """

prompt = f"""
{LEGAL_PROMPT}

STRICT INSTRUCTIONS:
- Answer ONLY from the provided legal context
- DO NOT make up laws or sections
- If answer is not clearly available, say:
  "I don't have enough information from the legal database."

Conversation History:
{conversation_context}

Current Question:
{query}

Legal Context:
{context}

Past User Cases:
{case_context}

Your Task:
1. Identify correct law/section
2. Explain in simple language
3. Give real-world example
4. Suggest practical actions
"""
response = llm.invoke(prompt)
memory.add("assistant",response.content)
return response.content