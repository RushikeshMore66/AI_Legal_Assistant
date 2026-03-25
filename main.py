from fastapi import FastAPI
from services.legal_service import process_query

app = FastAPI()

@app.post("/ask")
def ask(query: str):
    return {"answer": process_query(query)}
