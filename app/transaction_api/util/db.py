from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from typing import  TypeVar


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


DBModels= db.Model


ModelType= TypeVar("ModelType", bound= DBModels)