from core.llm import get_llm

def classify_intent(query: str):
    llm = get_llm()

    prompt = f"""
    Classify the legal intent of this query into one category:

    Categories:
    - criminal
    - civil
    - cyber
    - employment
    - constitutional
    - consumer

    Query: {query}

    Only return category name.
    """

    response = llm.invoke(prompt)
    return response.content.strip().lower().split("\n")[0].replace("the category is", "").strip()