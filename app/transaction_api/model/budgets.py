from uuid import uuid4
from app.transaction_api.util.db import DBModels
from sqlalchemy.sql import func
from sqlalchemy import  String, ForeignKey,DateTime, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column,relationship
from decimal import Decimal

from datetime import datetime,timedelta

from app.transaction_api.model.user import UserModel

class BudgetsModel(DBModels): 
    __tablename__= "budget"
    id:Mapped[str]=mapped_column("budgets_id", String(36), primary_key=True)
    user_id:Mapped[str]=mapped_column("user_id", String(36), ForeignKey("user.user_id"))
    
    name:Mapped[str]= mapped_column('name', String(255))
    amount:Mapped[Decimal]= mapped_column("amount",DECIMAL(10,2))
    

    start_date = mapped_column("start_date", DateTime(timezone=True), server_default=func.now())
    end_date = mapped_column("end_date",DateTime(timezone=True), onupdate=datetime.now)
    
    user:Mapped[UserModel]= relationship("UserModel", foreign_keys=[user_id])

    
    def __init__(self,user_id:str, name:str,amount: float, endDays: int) -> None:
        self.id= str(uuid4())
        
        self.user_id= user_id
        self.start_date= datetime.now()
        
        self.name= name
        self.amount= amount
        self.end_date= datetime.now() + timedelta(days=endDays)
    
        
    def update(self, name:str=None,amount: float =None, endDays: int=None):
        self.name= name if name!= None else self.name
        self.amount= amount if amount!= None else self.amount
        self.end_date= datetime.now() + timedelta(days=endDays) if endDays!= None else self.end_date
    
        
 
  
        