
from app.transaction_api.model.user import UserModel
from app.transaction_api.schemas.user import UserBaseSchema, UseResponseSchema

from app.transaction_api.model.account import AccountModel
from app.transaction_api.schemas.account import AccountBaseSchemas, AccountResponseSchema
# from sqlalchemy.exc import IntegrityError


from app.transaction_api.service.ModelMatcher import matherAccountModeWIthId
from pprint import pprint
# from uuid import UUID


from tests.views.ModelTestBase import ModelTestBase



class TestUser(ModelTestBase):
    
        
    def test_user_create_then_create_account(self):
        schemasUser= UserBaseSchema()
        schemasAccount= AccountBaseSchemas()
        schemasResponse= UseResponseSchema()
        schemasAccountResponse= AccountResponseSchema()
        
        
        """create user model """
        inputData= {
            "username":"dewa",
            "email":"dewa@gmail.com",
            "password":"somepassword"
        }
        createUserMode=schemasUser.load(inputData)
        self.session.add(createUserMode)
        """query user model"""
        queryUser:UserModel= self.session.query(UserModel).filter(UserModel.username == "dewa").first()
        result:UseResponseSchema = schemasResponse.dump(queryUser)
        pprint
        print(queryUser.id)
        inputCreateAccount={
            "user_id":queryUser.id,
            "account_type":"some type",
            "account_number":"some number",
            "balance":200_000
        }
 
        createAccount=  schemasAccount.load(inputCreateAccount)
        self.session.add(createAccount)
        
        queryAccount:AccountModel= self.session.query(AccountModel).filter(AccountModel.user_id == queryUser.id).first()
        response= schemasAccountResponse.dump(queryAccount)
        
        pprint(response, indent=2)
        assert queryAccount.user_id == queryUser.id
        assert queryAccount.balance == inputCreateAccount['balance']
        assert queryAccount.account_type == inputCreateAccount['account_type']
        assert queryAccount.account_number == inputCreateAccount['account_number']
        
        # testingGetUser= matherAccountModeWIthId(queryAccount.id)
        # testinParser= schemasAccountResponse.dump(testingGetUser)
        # pprint(testinParser, indent=2)
        
        

        """clean up"""
        self.session.delete(queryUser)
        self.session.delete(queryAccount)
        self.session.commit()