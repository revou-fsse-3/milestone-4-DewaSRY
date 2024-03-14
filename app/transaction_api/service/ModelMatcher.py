

from app.transaction_api.util.db import ModelType


def matherModel(model:ModelType,value:str= None)->ModelType : 
    if value == None : return 
    search = "%{}%".format(value)
    matchModel =   model.query.filter(model.name.like(search)).first() 
    return matchModel if matchModel else None




 