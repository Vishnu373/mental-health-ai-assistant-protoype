import os
import json
from utils.s3_utils import create_bucket, upload_file, delete_bucket
from rag.generate_chunks import generate_chunks
from rag.generate_embeddings import generate_embeddings

# --- Configuration ---
REGION = "us-east-1"

# Input bucket is ephemeral (unique each run)
INPUT_BUCKET_BASE = "mhai-knowledge-source"

# Output bucket is persistent (fixed name, reused for all runs)
OUTPUT_BUCKET_NAME = "mhai-embeddings-store"

LOCAL_INPUT_FILE = "data/input/knowledge_base.txt"
INPUT_KEY = "knowledge_base.txt"

LOCAL_CHUNKS_FILE = "data/output/knowledge_chunks.json"
LOCAL_EMBEDDINGS_FILE = "data/output/knowledge_embeddings.json"

CHUNKS_KEY = "chunks/knowledge_chunks.json"
OUTPUT_KEY = "embeddings/knowledge_embeddings.json"


def run_pipeline():
    """RAG pipeline with ephemeral input bucket and persistent output bucket."""
    input_bucket = None

    try:
        # --- 1. Create unique ephemeral input bucket ---
        print("Creating ephemeral input bucket...")
        input_bucket = create_bucket(INPUT_BUCKET_BASE, REGION, unique=True)
        print(f"Ephemeral input bucket: {input_bucket}")

        # --- 2. Persistent output bucket (no deletion) ---
        print("Ensuring persistent output bucket exists...")
        output_bucket = create_bucket(OUTPUT_BUCKET_NAME, REGION, unique=False)
        print(f"Persistent output bucket: {output_bucket}")

        # --- 3. Upload input file to input bucket ---
        upload_file(LOCAL_INPUT_FILE, input_bucket, INPUT_KEY)
        print(f"Uploaded {LOCAL_INPUT_FILE} to s3://{input_bucket}/{INPUT_KEY}")

        # --- 4. Generate chunks ---
        print("Generating chunks...")
        chunks = generate_chunks(
            input_bucket=input_bucket,
            input_key=INPUT_KEY,
            local_chunks_file=LOCAL_CHUNKS_FILE,
            region=REGION
        )
        print(f"Total chunks generated: {len(chunks)}")

        # --- 5. Generate embeddings and save to persistent output bucket ---
        print("Generating embeddings...")
        embeddings = generate_embeddings(
            chunks=chunks,
            output_bucket=output_bucket,
            output_key=OUTPUT_KEY,
            local_embeddings_file=LOCAL_EMBEDDINGS_FILE,
            region=REGION
        )
        print(f"Total embeddings generated: {len(embeddings)}")

        print("RAG pipeline completed successfully.")
        return embeddings

    finally:
        # --- 6. Safe cleanup: delete ephemeral input bucket ---
        print("Later use - integrating this logic")
        # if input_bucket:
        #     print(f"Cleaning up: deleting ephemeral input bucket {input_bucket}...")
        #     try:
        #         delete_bucket(input_bucket)
        #         print(f"Deleted ephemeral input bucket: {input_bucket}")
        #     except Exception as e:
        #         print(f"Warning: Failed to delete input bucket {input_bucket}. Error: {e}")

run_pipeline()
