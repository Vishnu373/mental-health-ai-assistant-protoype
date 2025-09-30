from urllib.parse import quote_plus
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy.pool import NullPool
import os
from langchain_aws import BedrockEmbeddings, ChatBedrock
from supabase import create_client, Client
import boto3

load_dotenv()

SUPABASE_DB_PASSWORD = quote_plus(os.getenv('SUPABASE_DB_PASSWORD'))
POOLER_DATABASE_URL = f"postgresql://postgres.exvookactbxsepivfpjx:{SUPABASE_DB_PASSWORD}@aws-1-ca-central-1.pooler.supabase.com:5432/postgres"
BUCKET_NAME = os.getenv("BUCKET_NAME")
KB_KEY = os.getenv("KB_KEY")
SUPABASE_URL=os.getenv("SUPABASE_URL")
SUPABASE_KEY=os.getenv("SUPABASE_KEY")

engine = create_engine(
    POOLER_DATABASE_URL,
    poolclass=NullPool,
    connect_args={
        "sslmode": "require",  # This is a requirement for Supabase connections
        "connect_timeout": 10
    }
)

s3 = boto3.client('s3')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
embedding_model = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")
llm_model = ChatBedrock(
    model_id="us.anthropic.claude-3-5-haiku-20241022-v1:0",
    model_kwargs={
        "temperature": 0.5,
        "max_tokens": 1000
    }
)
