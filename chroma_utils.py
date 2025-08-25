import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_aws import BedrockEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from typing import List

# Chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)

# Embedding
embedding_function = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")

# Vector store
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding_function
)

# Load PDF documents
def load_documents(folder_path: str) -> List[Document]:
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            loader = PyPDFLoader(file_path)

            docs = loader.load()
            split_docs = text_splitter.split_documents(docs)
            documents.extend(split_docs)
            print(f"Loaded and split: {filename}")
        else:
            print(f"Skipping non-PDF file: {filename}")
    return documents

# Index into Chroma
def index_documents(folder_path: str):
    try:
        docs = load_documents(folder_path)
        if docs:
            vectorstore.add_documents(docs)
            print(f"Successfully indexed {len(docs)} PDF chunks.")
        else:
            print("No PDFs found to index.")
    except Exception as e:
        print(f"Error during indexing: {e}")
