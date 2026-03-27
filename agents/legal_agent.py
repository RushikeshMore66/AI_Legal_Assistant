from core.llm import get_llm
from rag.retriever import retrieve_docs
from agents.intent_classifier import classify_intent
from utils.prompt import LEGAL_PROMPT
from utils.memory import memory
from utils.case_memory import save_cases, get_user_cases
from tools.fir_tool import generate_fir
from tools.complaint_tool import generate_complaint
from tools.action_tool import suggest_actions
from agents.tool_selector import select_tool

def is_relevant(query, docs):
    query_lower = query.lower()

    for d in docs:
        text = (d.page_content + str(d.metadata)).lower()
        if any(word in text for word in query_lower.split()):
            return True

    return False


def legal_agent(query):
    llm = get_llm()

    # 🔹 Save user input
    memory.add("User", query)

    conversation_context = memory.get_context()

    # 🔹 Case memory
    user_id = "default_user"
    save_cases(user_id, query)
    past_cases = get_user_cases(user_id)
    case_context = "\n".join(past_cases[-3:])

    # 🔹 Intent + tool
    intent = classify_intent(query)
    tool = select_tool(query, intent)

    # 🔥 TOOL EXECUTION
    if tool == "fir":
        result = generate_fir(query)
        memory.add("Assistant", result)
        return result

    if tool == "complaint":
        result = generate_complaint(query)
        memory.add("Assistant", result)
        return result

    # 🔹 Retrieval
    docs = retrieve_docs(query, intent)

    if not docs or not is_relevant(query, docs):
        return "I don't have enough information from the legal database."

    # 🔹 Context
    context = ""
    for d in docs:
        context += f"""
        Law: {d.metadata.get('law')}
        Section: {d.metadata.get('section')}
        Title: {d.metadata.get('title')}
        Content: {d.page_content}
        """

    # 🔹 Short mode
    short_mode = len(query.split()) < 5

    # 🔹 Prompt
    prompt = f"""
    {LEGAL_PROMPT}

    Conversation:
    {conversation_context}

    Question:
    {query}

    Context:
    {context}

    Past Cases:
    {case_context}

    Answer in this format ONLY:

    Explanation:
    Law:
    Use:
    Action:

    Keep answer under 120 words.
    """

    if short_mode:
        prompt += "\nGive very short answer (max 3 lines)."

    # 🔹 LLM
    response = llm.invoke(prompt)

    answer = response.content.strip()
    answer = answer[:800]

    # 🔹 Actions
    actions = suggest_actions(intent)
    actions_text = "\n- ".join(actions)

    final_response = f"""
    {answer}

    Recommended Actions:
    - {actions_text}

    ⚠️ This is general legal information, not legal advice.
    """

    # 🔹 Save memory
    memory.add("Assistant", final_response)

    return final_response