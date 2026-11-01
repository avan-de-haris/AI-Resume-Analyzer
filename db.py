import certifi
import ssl
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Database configuration
DATABASE_URL = (
    "mysql+pymysql://YuwhQJrgWGst6e8.root:bJDbpflhsqF2Z49k"
    "@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/test"
    "?ssl_ca=/etc/ssl/cert.pem"
)

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