

from app.transaction_api.model.user import UserModel
from app.transaction_api.model.transaction import TransactionsModel
from app.transaction_api.model.account import AccountModel


from app.transaction_api.util.db import ModelType


def matherModel(model:ModelType,value:str= None): 
    if value == None : return 
    search = "%{}%".format(value)
    matchModel =   model.query.filter(model.name.like(search)).first() 
    return matchModel.id if matchModel else 1



def matherAccountModeWIthId(accountId : str)-> AccountModel:
    return AccountModel.query.filter(AccountModel.id == accountId).first()

 