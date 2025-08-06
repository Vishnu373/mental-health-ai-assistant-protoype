import os
import json
from utils.bedrock_utils import generated_embeddings

def generate_embeddings(chunks, output_bucket, output_key, local_embeddings_file=None, region="us-east-1"):
    """
    Generates embeddings from text chunks and saves them locally + uploads to S3.

    Args:
        chunks (list): List of text chunks.
        output_bucket (str): S3 bucket to store embeddings.
        output_key (str): S3 key (path) for the embeddings file.
        local_embeddings_file (str): Optional local path to save embeddings.
        region (str): AWS region (default: us-east-1).

    Returns:
        list: List of dicts with "chunk" and "embedding".
    """

    # 1. Generate embeddings
    print("Generating embeddings for chunks...")
    embeddings = generated_embeddings(chunks, region)
    print(f"Total embeddings generated: {len(embeddings)}")

    # 2. Combine chunks and embeddings into structured data
    embeddings_data = [{"chunk": c, "embedding": e} for c, e in zip(chunks, embeddings)]

    # 3. Save locally if specified
    if local_embeddings_file:
        os.makedirs(os.path.dirname(local_embeddings_file), exist_ok=True)
        with open(local_embeddings_file, "w", encoding="utf-8") as f:
            json.dump(embeddings_data, f, ensure_ascii=False, indent=2)
        print(f"Embeddings saved locally at: {local_embeddings_file}")

    # 4. Upload embeddings to S3 (through s3_utils)
    from utils.s3_utils import save_to_s3
    save_to_s3(
        json.dumps(embeddings_data, ensure_ascii=False, indent=2),
        output_bucket,
        output_key
    )
    print(f"Embeddings uploaded to s3://{output_bucket}/{output_key}")

    return embeddings_data
