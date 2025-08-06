import os
import json
from s3_utils import create_bucket, upload_file, read_file, save_to_s3
from chunking_utils import chunk_text
from bedrock_utils import generated_embeddings

# Configuration
REGION = "us-east-1"
INPUT_BUCKET_BASE = "mhai-knowledge-source"
OUTPUT_BUCKET_BASE = "mhai-embeddings-store"
LOCAL_INPUT_FILE = "data/knowledge_base.txt"
INPUT_KEY = "knowledge_base.txt"
LOCAL_OUTPUT_FOLDER = "output"
LOCAL_EMBEDDINGS_FILE = "output/knowledge_embeddings.json"

# 0. Create input and output bucket (capture actual names)
print("Bucket creation...")
INPUT_BUCKET = create_bucket(INPUT_BUCKET_BASE, REGION)
OUTPUT_BUCKET = create_bucket(OUTPUT_BUCKET_BASE, REGION)

# 1. Upload local file to input bucket
print("Uploading the file to S3...")
upload_file(LOCAL_INPUT_FILE, INPUT_BUCKET, INPUT_KEY)
print(f"Uploaded {LOCAL_INPUT_FILE} to s3://{INPUT_BUCKET}/{INPUT_KEY}")

# 2. Read knowledge base from S3
print("Reading knowledge base from S3...")
raw_text = read_file(INPUT_BUCKET, INPUT_KEY)

# 3. Chunking
print("Chunking text...")
chunks = chunk_text(raw_text, chunk_size=256, chunk_overlap=30)
print(f"Total chunks created: {len(chunks)}")

# 4. Embeddings
print("Generating embeddings...")
embeddings = generated_embeddings(chunks, REGION)

# 5. Save embeddings locally
os.makedirs(os.path.dirname(LOCAL_EMBEDDINGS_FILE), exist_ok=True)
embeddings_data = [{"chunk": c, "embedding": e} for c, e in zip(chunks, embeddings)]
with open(LOCAL_EMBEDDINGS_FILE, "w", encoding="utf-8") as f:
    json.dump(embeddings_data, f, ensure_ascii=False, indent=2)
print(f"Embeddings saved locally at: {LOCAL_EMBEDDINGS_FILE}")

# 6. Upload embeddings to output S3 bucket
print("Uploading embeddings to S3...")
save_to_s3(json.dumps(embeddings_data, ensure_ascii=False, indent=2), 
           OUTPUT_BUCKET, "embeddings/knowledge_embeddings.json")
print(f"Embeddings uploaded to s3://{OUTPUT_BUCKET}/embeddings/knowledge_embeddings.json")
