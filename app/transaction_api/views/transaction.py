
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

blp= Blueprint("transactions", __name__, description="""
               transaction management 
               """)
DBS= DbModelService(TransactionsModel)

@blp.route("/transactions")
class TransactionView(MethodView):
    
    @jwt_required()
    @blp.response(HTTPStatus.OK, TransactionsResponseSchema(many=True))
    def get(self):
        """Retrieve a list of all transaction for the currently authenticated user's account """
        print("halloo")
        return DBS.getDbModalAll()
    
    @jwt_required()
    @blp.arguments(TransactionPayloadSchemas)
    @blp.response(HTTPStatus.CREATED, TransactionsResponseSchema)
    @blp.alt_response(HTTPStatus.NOT_ACCEPTABLE, 
                      description="failed to create transaction because the receiver have not enough balance",
                      )
    def post(self, item_data):
        """Initiate a new transactions (deposit, withdrawal or transfer )"""
        transactionModel:TransactionsModel=None
        schemas=TransactionCreateSchemas()
        try: 
            transactionModel= schemas.load(item_data)
        except ValueError as e:
            abort(HTTPStatus.NOT_ACCEPTABLE, message=f"the balance is not enough")
        print(item_data)
        try:
            return DBS.addModel(transactionModel)
        except Exception as  E:
            abort(HTTPStatus.NOT_ACCEPTABLE, message="error while insert the animal")

@blp.route("/transactions/<string:transaction_id>")
class TransactionViews(MethodView):
    
    @jwt_required()
    @blp.response(HTTPStatus.OK, TransactionsResponseSchema)
    def get(self,transaction_id ):
        """retrieval details of specific transaction by its ID"""
        return DBS.getDbModal(transaction_id)