
from uuid import uuid4
from app.transaction_api.util.db import db
from sqlalchemy.sql import func
from sqlalchemy import Integer, String, ForeignKey,UUID,DateTime, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, Relationship
# from app.transaction_api.service.ModelMatcher import SpeciesMather, GenderMather


class AccountModel(db.Model): 
    __tablename__= "account"
    id:Mapped[UUID]=mapped_column("account_id", UUID, default=uuid4, primary_key=True)
    user_id:Mapped[UUID]=mapped_column("user_id", UUID, ForeignKey("user.user_id"))
    
    account_type:Mapped[str]= mapped_column("account_type", String(50))
    account_number:Mapped[str]= mapped_column("account_number", String(50), unique=True)
    balance:Mapped[float]= mapped_column("balance",DECIMAL(10,2))
    
    created_at = mapped_column("created_at", DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column("updated_at",DateTime(timezone=True), onupdate=func.now())
    
    def __init__(self,user_id:str,  account_type:str, account_number:str,balance: float) -> None:
        self.user_id= user_id
        self.account_type= account_type
        self.account_number= account_number
        self.balance= balance
        
    def update(self, account_type:str, account_number:str,balance: float):
        self.account_type= account_type
        self.account_number= account_number
        self.balance= balance
        
        