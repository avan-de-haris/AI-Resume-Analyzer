from sqlalchemy import Column, Integer, String, Text, ForeignKey
from db import BASE

class User(BASE):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(128), nullable=False)

class Reports(BASE):
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    resume_text = Column(Text)
    result = Column(Text)


from db import engine

if __name__ == "__main__":
    print("Creating tables in TiDB...")
    BASE.metadata.create_all(bind=engine)
    print("Tables created successfully!")