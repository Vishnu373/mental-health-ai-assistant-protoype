from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import s3, supabase, BUCKET_NAME, KB_KEY, embedding_model

# 0. Get file from S3
def get_file():
    response = s3.get_object(Bucket=BUCKET_NAME, Key=KB_KEY)
    
    text = response['Body'].read().decode('utf-8')
    return text

# 1. Chunking
def splitter(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=750,
        chunk_overlap=256,
        length_function=len
    )

    chunks = text_splitter.split_text(text)
    return chunks

# 2. Embedding
def embed(chunks):
    embeddings = embedding_model.embed_documents(chunks)
    return embeddings

# 3. Vector store -> store chunks and embeddings in supabase
def store(chunks, embeddings):
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        data = {
            "content": chunk,
            "embedding": embedding,
            "metadata": {"chunk_index": i}
        }

        result = supabase.table("knowledge_base").insert(data).execute()

def run_pipeline():
    text = get_file()
    chunks = splitter(text)
    embeddings = embed(chunks)
    vectors = store(chunks, embeddings)
    
    print("Ingestion pipeline successfully!")

run_pipeline()