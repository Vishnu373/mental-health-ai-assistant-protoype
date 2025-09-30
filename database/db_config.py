from urllib.parse import quote_plus
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy.pool import NullPool

load_dotenv()

SUPABASE_DB_PASSWORD = quote_plus(os.getenv('SUPABASE_DB_PASSWORD'))
POOLER_DATABASE_URL = f"postgresql://postgres.exvookactbxsepivfpjx:{SUPABASE_DB_PASSWORD}@aws-1-ca-central-1.pooler.supabase.com:5432/postgres"

# Local setup
"""
DB_USER = "postgres"
DB_PORT = 5432
DB_NAME = "mhai"
DB_HOST = "127.0.0.1" 
DATABASE_URL = f"postgresql://{DB_USER}:{SUPABASE_DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"host": DB_HOST}
)
"""

# cloud setup
engine = create_engine(
    POOLER_DATABASE_URL,
    poolclass=NullPool,
    connect_args={
        "sslmode": "require",  # This is a requirement for Supabase connections
        "connect_timeout": 10
    }
)