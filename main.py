from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic_models import QueryInput, QueryResponse, DocumentInfo, DeleteFileRequest
from langchain_utils import get_rag_chain
from db_utils import insert_application_logs, get_chat_history, get_all_documents, insert_document_record, delete_document_record
from chroma_utils import index_document_to_chroma, delete_doc_from_chroma
import os
import uuid
import logging

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# Initialize FastAPI app
app = FastAPI()

@app.post("/chat", response_model=QueryResponse)
def chat(query_input: QueryInput):
    try:
        session_id = query_input.session_id or str(uuid.uuid4())
        logging.info(f"Session ID: {session_id}, User Query: {query_input.question}, Model: {query_input.model.value}")

        chat_history = get_chat_history(session_id)

        rag_chain = get_rag_chain(query_input.model.value)

        result = rag_chain.invoke({
            "input": query_input.question,
            "chat_history": chat_history
        })

        answer = result["answer"]

        insert_application_logs(session_id, query_input.question, answer, query_input.model.value)
        logging.info(f"Session ID: {session_id}, AI Response: {answer}")

        return QueryResponse(answer=answer, session_id=session_id, model=query_input.model.value)

    except Exception as e:
        logging.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Something went wrong while processing the chat.")