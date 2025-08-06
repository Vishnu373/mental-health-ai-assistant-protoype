from opensearchpy import OpenSearch
import os
from dotenv import load_dotenv

load_dotenv()

# Opensearch configuration
OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "your-opensearch-endpoint")
OPENSEARCH_PORT = 443
OPENSEARCH_USERNAME = os.getenv("OPENSEARCH_USERNAME", "your-username")
OPENSEARCH_PASSWORD = os.getenv("OPENSEARCH_PASSWORD", "your-password")
INDEX_NAME = "knowledge-embeddings"

# Opensearch client for reusability - maybe in future
def get_opensearch_client():
    client = OpenSearch(
        hosts=[{"host": OPENSEARCH_HOST, "port": OPENSEARCH_PORT}],
        http_auth=(OPENSEARCH_USERNAME, OPENSEARCH_PASSWORD),
        use_ssl=True,
        verify_certs=True
    )
    return client

# Indexing logic
def knn_index(client, index_name=INDEX_NAME, vector_dim=1024):
    # Checks for existence
    if client.indices.exists(index=index_name):
        print(f"Index '{index_name}' already exists.")
        return

    index_body = {
        "settings": {
            "index.knn": True
        },

        "mappings": {
            "properties": {
                "chunk": {"type": "text"},
                "embedding": {
                    "type": "knn_vector",
                    "dimension": vector_dim,
                    "method": {
                        "name": "hnsw",
                        "space_type": "l2",
                        "engine": "nmslib"
                    }
                }
            }
        }
    }

    client.indices.create(index=index_name, body=index_body)
    print(f"Index '{index_name}' created successfully!")

# knn-index created + knowlege_embeddings.json are stored
def insert_document(client, doc, index_name=INDEX_NAME):
    response = client.index(index=index_name, body=doc)
    return response
