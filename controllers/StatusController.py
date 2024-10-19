from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
import os

from models.Models import Status

load_dotenv()
database = os.getenv("DATABASE")


class StatusController:
    def __init__(self, db_url):
        self.engine = create_engine(database)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
       
       
    # Read Methods
    
    def read_all_status(self):
        session = self.SessionLocal()
        result = session.query(Status).all()
        session.close()
        return result   