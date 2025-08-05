from s3_utils import read_file
from bedrock_utils import generated_embeddings
import json
import os

BUCKET_NAME = "mhai-clinical-reports"
FILE_KEY = "data-folder/knowledge_base.txt"
OUTPUT_PATH = "rag/embeddings/knowledge_embeddings.json"
REGION = "us-east-1"

print("Reading knowledge base from S3...")
chunks = read_file(BUCKET_NAME, FILE_KEY)

print(f"Total chunks: {len(chunks)}. Generating embeddings...")
embeddings = generated_embeddings(chunks, REGION)

data = [
    {"chunk": chunk, "embedding": embedding}
    for chunk, embedding in zip(chunks, embeddings)
]

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

with open(OUTPUT_PATH, "w") as f:
    json.dump(data, f)

print(f"✅ Embeddings generated and saved to {OUTPUT_PATH} (JSON format)")
