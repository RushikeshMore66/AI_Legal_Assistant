def select_tool(query, intent):
    query = query.lower()

    if "fir" in query or "police complaint" in query:
        return "fir"

    if "complaint" in query:
        return "complaint"

    return "none"