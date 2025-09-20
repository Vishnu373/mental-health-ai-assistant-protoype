from langchain_aws import BedrockEmbeddings
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from services.models import embedding_model

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Retrieve relevant therapy content
def retrieve(query, match_count=3):
    results = supabase.rpc(
        'match_data', {
            'query_embedding': embedding_model.embed_query(query),
            'match_threshold': 0.1,
            'match_count': match_count
        }
    ).execute()

    results = results.data
    all_matches = [result.get('content', '') for result in results if result.get('content')]
    all_matches = "\n\n".join(all_matches)

    return all_matches