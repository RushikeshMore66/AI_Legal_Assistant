import os
from rag.embedding import get_embeddings
import re
from pypdf import PdfReader
from langchain_community.vectorstores import FAISS

DATA_PATH = "data"
DB_PATH = "db"


# 🔹 Load PDF
def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"

    return text


# 🔹 Detect Sections / Articles
def split_into_sections(text, law_name):
    if law_name == "Constitution":
        pattern = r"(Article\s+\d+.*?)(?=Article\s+\d+|$)"
    else:
        pattern = r"(Section\s+\d+.*?)(?=Section\s+\d+|$)"

    matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
    return matches


# 🔹 Extract Metadata
def extract_metadata(section_text, law_name):
    number_match = re.search(r"(Section|Article)\s+(\d+)", section_text, re.IGNORECASE)
    number = number_match.group(2) if number_match else "Unknown"

    title = section_text.split("\n")[0]

    return {
        "law": law_name,
        "section": number,
        "title": title
    }


# 🔹 Create Documents
def create_documents():
    documents = []

    for file in os.listdir(DATA_PATH):
        if file.endswith(".pdf"):
            path = os.path.join(DATA_PATH, file)

            print(f"Processing: {file}")

            text = load_pdf(path)

            if "constitution" in file.lower():
                law_name = "Constitution"
            elif "ipc" in file.lower():
                law_name = "IPC"
            else:
                law_name = "General Law"

            sections = split_into_sections(text, law_name)

            if not sections:
                sections = [text]  # fallback
            for sec in sections:
                metadata = extract_metadata(sec, law_name)

                documents.append({
                    "content": sec,
                    "metadata": metadata
                })

    return documents


# 🔹 Build Vector DB
def build_db(docs):
    texts = [d["content"] for d in docs]
    metas = [d["metadata"] for d in docs]

    embeddings = get_embeddings()

    db = FAISS.from_texts(texts, embeddings, metadatas=metas)
    db.save_local(DB_PATH)

    print("✅ DB Created with HuggingFace embeddings!")


# 🔹 Run
if __name__ == "__main__":
    docs = create_documents()
    build_db(docs)