from langchain_huggingface import HuggingFaceEmbeddings
import os

try:
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    print("Successfully loaded embeddings locally")
except Exception as e:
    print(f"Error loading locally: {e}")
