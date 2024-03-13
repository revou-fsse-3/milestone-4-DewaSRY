# from app.model import engine, Base, Article, Author, Session
# from app.transaction_api.util.db import DBModels


from app.transaction_api.model.user import UserModel
from app.transaction_api.schemas.user import UserBase
from sqlalchemy.exc import IntegrityError
import pytest

from pprint import pprint

from tests.views.ModelTestBase import ModelTestBase


class TestUser(ModelTestBase):
    
    def test_user_first(self):
        testUser= UserModel("dewa", "dewa@gmail.com", "somepassword")
        self.session.add(testUser)
        testUser:UserModel= self.session.query(UserModel).filter(UserModel.username == "dewa").first()
        schemas= UserBase()
        result = schemas.dump(testUser)
        pprint(result, indent=2)
        testUser.update(username="new dewa")
        self.session.add(testUser)
        self.session.commit()
        result_2 = schemas.dump(testUser)
        pprint(result_2, indent=2)
        
        print(testUser.updated_at)
        
        assert testUser.username =="new dewa"
        
        