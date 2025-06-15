from sqlalchemy import create_engine
from app.models import Base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def create_all_tables():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
