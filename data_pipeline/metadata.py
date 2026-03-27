def detect_intent(text):
    text = text.lower()

    if any(word in text for word in ["murder", "kill", "theft"]):
        return "criminal"

    if any(word in text for word in ["hack", "cyber"]):
        return "cyber"

    if "article" in text:
        return "constitutional"

    return "general"


def enrich(section, law_name):
    return {
        "law": law_name,
        "section": section["title"],
        "intent": detect_intent(section["content"]),
        "preview": section["content"][:200]
    }
    