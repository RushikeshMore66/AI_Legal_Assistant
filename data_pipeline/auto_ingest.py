from langchain.vectorstores import FAISS
from langchain.schema import Document

from rag.embeddings import get_embeddings
from data_pipeline.pdf_loader import extract_text
from data_pipeline.section_parser import split_sections
from data_pipeline.metadata import enrich


def ingest_pdf(file_path, law_name):
    print(f"📄 Processing: {file_path}")

    text = extract_text(file_path)

    sections = split_sections(text)

    if not sections:
        print("⚠️ No sections detected, fallback to full text")
        sections = [{"title": "Full Document", "content": text}]

    docs = []

    for sec in sections:
        metadata = enrich(sec, law_name)

        doc = Document(
            page_content=sec["content"],
            metadata=metadata
        )

        docs.append(doc)

    db = FAISS.from_documents(docs, get_embeddings())
    db.save_local("db")

    print(f"✅ Stored {len(docs)} sections")