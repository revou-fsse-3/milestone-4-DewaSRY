
from app.transaction_api.model.user import UserModel
from app.transaction_api.schemas.user import UserBaseSchema, UseResponseSchema
from sqlalchemy.exc import IntegrityError

from pprint import pprint

from tests.views.ModelTestBase import ModelTestBase



class TestUser(ModelTestBase):
    
        
    def test_user_create_and_update(self):
        schemas= UserBaseSchema()
        schemasResponse= UseResponseSchema()
        
        
        """create user model """
        inputData= {
            "username":"dewa",
            "email":"dewa@gmail.com",
            "password":"somepassword"
        }
        newName= "new dewa"
        createUserMode=schemas.load(inputData)
        self.session.add(createUserMode)
        """query user model"""
        queryUser:UserModel= self.session.query(UserModel).filter(UserModel.username == "dewa").first()
        result:UseResponseSchema = schemasResponse.dump(queryUser)
        
        assert queryUser.username == inputData["username"]
        assert queryUser.email == inputData["email"]
        assert queryUser.password == inputData["password"]
        
        assert result["username"] == inputData["username"]
        assert result['email'] == inputData["email"]
        assert result['password'] == inputData["password"]
        
        """update user data"""
        queryUser.update(username=newName)
        self.session.add(queryUser)
        self.session.commit()
        """query user model after update"""
        queryUserSecond:UserModel= self.session.query(UserModel).filter(UserModel.username== newName).first()
        resultTwo = schemasResponse.dump(queryUserSecond)
        
        
        assert queryUserSecond.username ==newName
        assert queryUserSecond.email == inputData["email"]
        assert queryUserSecond.password == inputData["password"]
        
        assert resultTwo["username"] == newName
        assert resultTwo['email'] == inputData["email"]
        assert resultTwo['password'] == inputData["password"]
        
        self.session.delete(queryUserSecond)
        self.session.commit()