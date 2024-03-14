
from uuid import uuid4
from app.transaction_api.util.db import DBModels
from sqlalchemy.sql import func
from sqlalchemy import Integer, String, ForeignKey,DateTime, DECIMAL,Integer
from sqlalchemy.orm import Mapped, mapped_column,relationship
from datetime import datetime
from decimal import Decimal


from app.transaction_api.model.transaction_categories import TransactionCategoryModel
from app.transaction_api.service.ModelMatcher import matherModel


class TransactionsModel(DBModels): 
    __tablename__= "transaction"
    id:Mapped[str]=mapped_column("transaction_id", String(36), primary_key=True)
    
    from_account_id:Mapped[str]= mapped_column("from_account_id",String(36), ForeignKey("account.account_id"))
    to_account_id:Mapped[str]= mapped_column("to_account_id",String(36), ForeignKey("account.account_id"))
    
    amount:Mapped[Decimal]= mapped_column("amount",DECIMAL(10,2))
    type_id:Mapped[int]= mapped_column("category_id", Integer,ForeignKey("transaction_category.category_id") )
    description:Mapped[str]= mapped_column("description", String(250))
    
    created_at = mapped_column("created_at", DateTime(timezone=True), server_default=func.now())
    type:Mapped[TransactionCategoryModel]= relationship("TransactionCategoryModel", foreign_keys=[type_id], backref="transaction")
    
    
    def __init__(self,from_account_id:str, to_account_id:str, amount: float, type: str,description:str) -> None:
        typeId= self.matherModelTransactionCategory(type)
        if typeId == None:
            raise ValueError(f"transaction type : '{type}' is not found")
        
        self.id= str(uuid4())
        self.from_account_id= from_account_id
        self.to_account_id= to_account_id
        self.amount= amount
        self.type_id= typeId.id
        self.description= description
        self.created_at= datetime.now()
    
    def matherModelTransactionCategory(self, value:str)->TransactionCategoryModel :
        return matherModel(TransactionCategoryModel, value=value)


        
