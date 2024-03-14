



from flask_smorest import Blueprint, abort
from flask.views import MethodView
from http import HTTPStatus
from flask_jwt_extended import jwt_required

from app.transaction_api.service.DbModelService import DbModelService
from app.transaction_api.schemas.transaction import (
        TransactionsResponseSchema,
        TransactionCreateSchemas,
        TransactionPayloadSchemas
    )

from app.transaction_api.model.transaction import TransactionsModel
from app.transaction_api.model.account import AccountModel
from app.transaction_api.util.JWTGetters import getCurrentAuthId

blp= Blueprint("bills", __name__, description="""
               bills management 
               """)
DBS= DbModelService(TransactionsModel)


@blp.route("/bills")
class billsViews(MethodView):
    def post(self):
        "Create a new bills payment for specific biller"
        pass
    
    def get(self):
        "Retrieve all bills scheduled bill payment"
        pass

@blp.route("/bills<int:bills_id>")
class billsViews(MethodView):
    
    def put(self,bills_id):
        "update an existing bills"
        pass
    
    def delete(self,bills_id):
        "cancel a scheduled  bill payment "
        pass