import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env

def get_server_access():
    # Create SQLAlchemy connection string
    conn_str = (
        f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    )
    engine = create_engine(url = conn_str)
    return engine



