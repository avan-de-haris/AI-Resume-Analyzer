from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Database configuration
DATABASE_URL = "mysql+mysqldb://YuwhQJrgWGst6e8.root:bJDbpflhsqF2Z49k@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/test?ssl_mode=VERIFY_IDENTITY&ssl_ca=/etc/ssl/cert.pem"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Adjust the pool size as needed
    connect_args={
        "ssl": {
            "ssl": True,
        }
    }
)

SessionLocal = sessionmaker(bind=engine)
BASE = declarative_base()