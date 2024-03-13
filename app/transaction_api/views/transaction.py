
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from http import HTTPStatus


from app.transaction_api.service.DbModelService import DbModelService
from app.transaction_api.schemas.transaction import (
        TransactionsBaseSchemas,
        TransactionsResponseSchema
    )
from app.transaction_api.model.transaction import TransactionsModel




blp= Blueprint("transactions", __name__, description="""transaction management """)
DBS= DbModelService(TransactionsModel)

@blp.route("/transactions")
class TransactionView(MethodView):
    
    @blp.response(HTTPStatus.OK, TransactionsResponseSchema(many=True))
    def get():
        """Retrieve a list of all transaction for the currently authenticated user's account """
        return DBS.getDbModalAll()
    @blp.arguments(TransactionsBaseSchemas)
    @blp.response(HTTPStatus.CREATED, TransactionsResponseSchema)
    def post(self, item_data):
        """Initiate a new transactions (deposit, withdrawal or transfer )"""
        transactionModel:TransactionsModel=None
        try: 
            transactionModel= TransactionsBaseSchemas().load(**item_data)
        except ValueError as e:
            abort(HTTPStatus.NOT_ACCEPTABLE, message="the balance is not enough")
            
        try:
            return DBS.addModel(transactionModel)
        except Exception as  E:
            abort(HTTPStatus.NOT_ACCEPTABLE, message="error while insert the animal")


@blp.route("/transactions/<string:transaction_id>")
class TransactionViews(MethodView):
    @blp.response(HTTPStatus.OK, TransactionsResponseSchema)
    def get(self,transaction_id ):
        """retrieval details of specific transaction by its ID"""
        return DBS.getDbModal(transaction_id)