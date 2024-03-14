from uuid import uuid4
from app.transaction_api.util.db import DBModels
from sqlalchemy import  String,Integer
from sqlalchemy.orm import Mapped, mapped_column


class AcountTypeModel(DBModels): 
    __tablename__= "account_type"
    id:Mapped[int]=mapped_column("type_id",Integer , primary_key=True)
    name:Mapped[str]= mapped_column("name", String(100), unique=True)

    def __init__(self, name:str) -> None:
        self.name= name
        
        
    def update(self, name:str= None):
        self.name= name if name !=None else self.name
   
 
    def __repr__(self) -> str:
        return f"{self.name}"