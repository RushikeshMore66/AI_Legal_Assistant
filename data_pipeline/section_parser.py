import re

def split_sections(text):
    pattern = r"(Section\s+\d+[A-Z]?|Article\s+\d+[A-Z]?)"

    parts = re.split(pattern, text)

    sections = []

    for i in range(1, len(parts), 2):
        title = parts[i]
        content = parts[i+1] if i+1 < len(parts) else ""

        sections.append({
            "title": title.strip(),
            "content": content.strip()
        })

    return sections