
from uuid import uuid4
from app.transaction_api.util.db import DBModels
from sqlalchemy.sql import func
from sqlalchemy import Integer, String, ForeignKey,UUID,DateTime
from sqlalchemy.orm import Mapped, mapped_column, Relationship


class UserModel(DBModels): 
    __tablename__= "user"
    id:Mapped[UUID]=mapped_column("user_id", UUID, default=uuid4, primary_key=True)
    
    username:Mapped[str]=mapped_column("username", String(50))
    email:Mapped[str]=mapped_column("email", String(50))
    password:Mapped[str]=mapped_column("password_hash", String(250))
    
    created_at = mapped_column("created_at", DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column("updated_at",DateTime(timezone=True), onupdate=func.now())
    
    def __init__(self, username:str, email:str, password:str) -> None:
        self.username= username
        self.email=email
        self.password= password