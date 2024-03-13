# from app.model import engine, Base, Article, Author, Session
from app.transaction_api.util.db import DBModels

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///test/data.db")
Session = sessionmaker(bind=engine)

class ModelTestBase(unittest.TestCase):
    
    def setup_class(self):
        DBModels.metadata.create_all(engine)
        self.session = Session()
   
    def teardown_class(self):
        self.session.rollback()
        self.session.close()
    
