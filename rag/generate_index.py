import json
from utils.s3_utils import load_embeddings
from utils.opensearch_utils import get_opensearch_client, knn_index, insert_document

# S3 output bucket configuration
S3_BUCKET = "mhai-embeddings-store"
S3_KEY = "embeddings/knowledge_embeddings.json"

# 1. Connect to OpenSearch
client = get_opensearch_client()

# 2. Load embeddings from S3
embeddings_data = load_embeddings(S3_BUCKET, S3_KEY)

vector_dim = len(embeddings_data[0]["embedding"])
print(f"Loaded {len(embeddings_data)} embeddings from S3. Vector dim: {vector_dim}")

# 3. Create index if not exists
knn_index(client, vector_dim=vector_dim)

# 4. Index documents
for i, item in enumerate(embeddings_data):
    doc = {
            "chunk": item["chunk"],
            "embedding": item["embedding"]
        }
    insert_document(client, doc)
    if i % 50 == 0:
        print(f"Indexed {i} documents...")

print("All embeddings indexed successfully in OpenSearch!")


