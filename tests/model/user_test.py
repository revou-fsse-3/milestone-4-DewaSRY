# from app.model import engine, Base, Article, Author, Session
# from app.transaction_api.util.db import DBModels


from app.transaction_api.model.user import UserModel
from sqlalchemy.exc import IntegrityError
import pytest



from tests.model.contest import ModelTestBase



class TestUser(ModelTestBase):
    def UserTest(self):
        testUser= UserModel("dewa", "dewa@gmail.com", "somepassword")
        self.session.add(testUser)
        testUser:UserModel= UserModel.query.filter(UserModel.username == "dewa").first()
        print(testUser.username)
        assert testUser.username =="dewa"
        self.assertEqual(testUser.username == "dewa")