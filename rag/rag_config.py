import os
from langchain_aws import BedrockEmbeddings, ChatBedrock
from supabase import create_client, Client
import boto3
from dotenv import load_dotenv

load_dotenv()

# S3 bucket - Knowledge base
s3 = boto3.client('s3')
BUCKET_NAME = os.getenv("BUCKET_NAME")
KB_KEY = os.getenv("KB_KEY")

# Vector store - Pg vector
SUPABASE_URL=os.getenv("SUPABASE_URL")
SUPABASE_KEY=os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

embedding_model = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")

llm_model = ChatBedrock(
    model_id="us.anthropic.claude-3-5-haiku-20241022-v1:0",
    model_kwargs={
        "temperature": 0.5,
        "max_tokens": 1000
    }
)
