from urllib.parse import quote_plus
from sqlalchemy import create_engine

DB_USER = "postgres"
DB_PASSWORD = quote_plus("PostgresSQL123@")
DB_HOST = "127.0.0.1" 
DB_PORT = 5432
DB_NAME = "mhai"
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"host": DB_HOST}
)
