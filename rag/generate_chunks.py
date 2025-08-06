import os
import json
from utils.s3_utils import read_file
from utils.chunking_utils import chunk_text

def generate_chunks(input_bucket, input_key, local_chunks_file=None, region="us-east-1"):
    """
    Reads a file from S3, performs chunking, and optionally saves chunks locally.
    
    Args:
        input_bucket (str): Name of the S3 input bucket.
        input_key (str): Key of the file in the input bucket.
        local_chunks_file (str): Optional path to save chunks locally.
        region (str): AWS region (default: us-east-1).

    Returns:
        list: List of chunked text segments.
    """
    # 1. Read knowledge base from S3
    print(f"Reading file from S3: s3://{input_bucket}/{input_key}")
    raw_text = read_file(input_bucket, input_key)

    # 2. Perform chunking
    print("Performing text chunking...")
    chunks = chunk_text(raw_text, chunk_size=256, chunk_overlap=30)
    print(f"Total chunks created: {len(chunks)}")

    # 3. Save locally if needed
    if local_chunks_file:
        os.makedirs(os.path.dirname(local_chunks_file), exist_ok=True)
        with open(local_chunks_file, "w", encoding="utf-8") as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)
        print(f"Chunks saved locally at: {local_chunks_file}")

    return chunks
