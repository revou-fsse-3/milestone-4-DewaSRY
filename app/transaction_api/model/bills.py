from uuid import uuid4
from app.transaction_api.util.db import DBModels
from sqlalchemy.sql import func
from sqlalchemy import  String, ForeignKey,DateTime, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column,relationship
from decimal import Decimal

from datetime import datetime,timedelta

from app.transaction_api.model.user import UserModel
from app.transaction_api.model.account import AccountModel

class BillsModel(DBModels): 
    __tablename__= "bill"
    id:Mapped[str]=mapped_column("bill_id", String(36), primary_key=True)
    
    user_id:Mapped[str]=mapped_column("user_id", String(36), ForeignKey("user.user_id"))
    account_id:Mapped[str]=mapped_column("account_id", String(36), ForeignKey("account.account_id"))
    
    biller_name:Mapped[str]= mapped_column("biller_name", String(250) )
    amount:Mapped[Decimal]= mapped_column("amount",DECIMAL(10,2))
    
    due_date = mapped_column("due_date", DateTime(timezone=True), server_default=func.now())
    user:Mapped[UserModel]= relationship("UserModel", foreign_keys=[user_id])
    account:Mapped[AccountModel]= relationship("AccountModel", foreign_keys=[account_id])

    
    def __init__(self,user_id:str,account_id:str, biller_name:str,amount: float, daysOfBills:int) -> None:
        self.id= str(uuid4())
        self.user_id= user_id
        self.account_id= account_id
        
        self.biller_name= biller_name
        self.amount= amount
        
        self.due_date= datetime.now() + timedelta(days=daysOfBills)
        
    def update(self, biller_name:str=None,amount: float=None, daysOfBills:int=None):
        self.biller_name= biller_name if biller_name!= None else self.biller_name
        self.amount= amount if amount!= None else self.amount
        self.due_date= datetime.now() + timedelta(days=daysOfBills) if daysOfBills!= None else self.due_date
                
        
        
 
        