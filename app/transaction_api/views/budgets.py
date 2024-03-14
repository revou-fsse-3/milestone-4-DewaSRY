



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

blp= Blueprint("budgets", __name__, description="""
               budgets management 
               """)
DBS= DbModelService(TransactionsModel)


@blp.route("/budgets")
class BudgetsViews(MethodView):
    def post(self):
        "Create a new budgets for specific category"
        pass
    def get(self):
        "Retrieve all budgets crete by the user"
        pass

@blp.route("/budgets<int:budgets_id>")
class BudgetsViews(MethodView):
    
    def put(self,budgets_id):
        "update an existing budgets"
        pass