
from uuid import uuid4
from app.transaction_api.util.db import DBModels
from sqlalchemy.sql import func
from sqlalchemy import Integer, String,DateTime,BINARY
from sqlalchemy.orm import Mapped, mapped_column, Relationship
from datetime import datetime
from passlib.hash import pbkdf2_sha256

class UserModel(DBModels): 
    __tablename__= "user"
    id:Mapped[str]=mapped_column("user_id", String(36), primary_key=True)
    
    
    username:Mapped[str]=mapped_column("username", String(50))
    email:Mapped[str]=mapped_column("email", String(50))
    password:Mapped[str]=mapped_column("password_hash", String(200))
    
    created_at = mapped_column("created_at", DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column("updated_at",DateTime(timezone=True), onupdate=datetime.now)
    
    def __init__(self, username:str, email:str, password:str) -> None:
        self.id= str(uuid4())
        self.created_at= datetime.now()
        self.updated_at= datetime.now()
        self.username= username
        self.email=email
        self.password= pbkdf2_sha256.hash(password) 
        
        
    def update(self,username:str=None, email:str=None, password:str=None):
        self.username= username if username != None else self.username
        self.email=email if email != None else self.email
        self.password= pbkdf2_sha256.hash(password)  if password != None else self.password
        self.updated_at= datetime.now()
    
        