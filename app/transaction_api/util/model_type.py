"""model type """
from typing import  TypeVar

# from app.tra import db

"""test"""
ModelType= TypeVar("ModelType", bound= db.Model)