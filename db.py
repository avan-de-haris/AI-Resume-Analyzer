import os
import certifi
import ssl
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

ssl_context = ssl.create_default_context(
    cafile=certifi.where()
)


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Adjust the pool size as needed
    connect_args={
        "ssl": {
            "ssl_context": ssl_context
        }
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
BASE = declarative_base()