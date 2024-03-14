
from uuid import uuid4
from app.transaction_api.util.db import DBModels
from sqlalchemy.sql import func
from sqlalchemy import  String, ForeignKey,DateTime, DECIMAL, Integer
from sqlalchemy.orm import Mapped, mapped_column,relationship
from decimal import Decimal

from datetime import datetime

from app.transaction_api.model.user import UserModel
from app.transaction_api.model.account_type import AcountTypeModel
from app.transaction_api.service.ModelMatcher import matherModel

class AccountModel(DBModels): 
    __tablename__= "account"
    id:Mapped[str]=mapped_column("account_id", String(36), primary_key=True)
    
    user_id:Mapped[str]=mapped_column("user_id", String(36), ForeignKey("user.user_id"))
    
    type_id:Mapped[int]=mapped_column("type_id",Integer, ForeignKey("account_type.type_id"))
    
    account_number:Mapped[str]= mapped_column("account_number", String(50), unique=False)
    balance:Mapped[Decimal]= mapped_column("balance",DECIMAL(10,2))
    
    created_at = mapped_column("created_at", DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column("updated_at",DateTime(timezone=True), onupdate=datetime.now)
    
    # user:Mapped[UserModel]= relationship("UserModel", foreign_keys=[user_id])
    account_type:Mapped[AcountTypeModel]= relationship("AcountTypeModel", foreign_keys=[type_id], backref="account")

    
    def __init__(self,user_id:str, account_type:str, account_number:str,balance: float) -> None:
        self.id= str(uuid4())
        self.user_id= user_id
        accountType:AcountTypeModel= self.matherModelAcountTypeModel(account_type)
        if accountType == None:
            raise ValueError(f"account type : '{account_type}' is not found")
        self.type_id= accountType.id
        
        self.account_number= account_number
        self.balance= balance
        
        self.created_at= datetime.now()
        self.updated_at= datetime.now()
    def matherModelAcountTypeModel(self, value:str)-> AcountTypeModel:
        return matherModel(AcountTypeModel, value= value)
        
    def update(self, account_type:int= None, account_number:str=None,balance: float=None):
        if account_type!= None: 
            accountType:AcountTypeModel= self.matherModelAcountTypeModel(account_type)
            if accountType == None:
                raise ValueError(f"account type : '{account_type}' is not found")
            self.type_id= accountType.id


        self.balance= balance if balance!= None else self.balance
        self.account_number= account_number if account_number!= None else self.account_number
        self.updated_at= datetime.now()
        
    def transfer(self, amount: float, to_account_id:str, ):
        decimalAmount=Decimal(amount)
        
        if decimalAmount.compare(self.balance) > 0:
            """if the amount to transfer is greater the current balance app will throw error """
            raise ValueError(f"acount with id : {self.id} have not enough money, ")
        self.balance= self.balance - decimalAmount;
        
        receiver:AccountModel= self.query.get_or_404(to_account_id)
        receiver.receive(amount= decimalAmount)
    
    def receive(self,  amount: Decimal):
        self.balance= self.balance + amount
        
    def __repr__(self) -> str:
        return f"{self.user_id} {self.balance} {self.account_type}"
        