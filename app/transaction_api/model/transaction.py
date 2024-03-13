
from uuid import uuid4
from app.transaction_api.util.db import DBModels
from sqlalchemy.sql import func
from sqlalchemy import Integer, String, ForeignKey,UUID,DateTime, DECIMAL,BINARY
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class TransactionsModel(DBModels): 
    __tablename__= "transaction"
    id:Mapped[int]=mapped_column("transaction_id", Integer, primary_key=True)
    
    from_account_id:Mapped[str]= mapped_column("from_account_id",String(36), ForeignKey("account.account_id"))
    to_account_id:Mapped[str]= mapped_column("to_account_id",String(36), ForeignKey("account.account_id"))
    
    amount:Mapped[float]= mapped_column("amount",DECIMAL(10,2))
    type:Mapped[str]= mapped_column("type", String(30))
    description:Mapped[str]= mapped_column("description", String(250))
    

    created_at = mapped_column("created_at", DateTime(timezone=True), server_default=func.now())
    
    def __init__(self,from_account_id:UUID, to_account_id:UUID, amount: float, type: str,description:str) -> None:
        self.id= str(uuid4())
        self.from_account_id= from_account_id
        self.to_account_id= to_account_id
        self.amount= amount
        self.type= type
        self.description= description
        self.created_at= datetime.now()

        
