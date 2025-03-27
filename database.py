# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "postgresql://postgres:Mm%40%4082651@localhost/socialdb"

# Create engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Create the tables if they don't exist
Base.metadata.create_all(engine)

def get_session():
    return Session()