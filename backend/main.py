from fastapi import FastAPI, HTTPException
from backend.pydantic_models import QueryInput, QueryResponse
from backend.langchain_utils import get_rag_chain
from backend.db_utils import insert_application_logs, get_chat_history
from backend.chroma_utils import load_documents, index_documents
import os
import uuid
import logging
import traceback
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Mental Health Chatbot API is running"}

@app.post("/chat", response_model=QueryResponse)
def chat(query_input: QueryInput):
    try:
        session_id = query_input.session_id or str(uuid.uuid4())
        logging.info(f"Session ID: {session_id}, User Query: {query_input.question}, Model: {query_input.model.value}")

        chat_history = get_chat_history(session_id)
        rag_chain = get_rag_chain()

        result = rag_chain.invoke({
            "input": query_input.question,
            "chat_history": chat_history
        })

        # # 👇 DEBUG PRINT
        # print("DEBUG RESULT:", result)

        answer = result.get("answer", None)
        if not answer:
            raise ValueError(f"Unexpected chain output: {result}")

        insert_application_logs(session_id, query_input.question, answer, query_input.model.value)
        logging.info(f"Session ID: {session_id}, AI Response: {answer}")

        return QueryResponse(answer=answer, session_id=session_id, model=query_input.model.value)

    except Exception as e:
        print("ERROR in /chat endpoint:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Something went wrong while processing the chat.")