
from uuid import uuid4
from app.transaction_api.util.db import DBModels
from sqlalchemy.sql import func
from sqlalchemy import Integer, String, ForeignKey,UUID,DateTime, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, Relationship


class TransactionsModel(DBModels): 
    __tablename__= "transaction"
    id:Mapped[int]=mapped_column("transaction_id", Integer, primary_key=True)
    
    from_account_id:Mapped[UUID]= mapped_column("from_account_id",UUID, ForeignKey("account.account_id"))
    to_account_id:Mapped[UUID]= mapped_column("to_account_id",UUID, ForeignKey("account.account_id"))
    
    amount:Mapped[float]= mapped_column("amount",DECIMAL(10,2))
    type:Mapped[str]= mapped_column("type", String(30))
    description:Mapped[str]= mapped_column("description", String(250), nullable=False)
    
    created_at = mapped_column("created_at", DateTime(timezone=True), server_default=func.now())
    
    def __init__(self,from_account_id:str, to_account_id:str, amount: float, type: str,description:str) -> None:
        self.from_account_id= from_account_id
        self.to_account_id= to_account_id
        self.amount= amount
        self.type= type
        self.description= description
        