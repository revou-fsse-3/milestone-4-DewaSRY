
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from http import HTTPStatus
from flask_jwt_extended import jwt_required,get_jwt
from sqlalchemy import or_
from app.transaction_api.service.DbModelService import DbModelService
from app.transaction_api.schemas.transaction import (
        TransactionsResponseSchema,
        TransactionCreateSchemas,
        TransactionPayloadSchemas
    )

from app.transaction_api.model.transaction import TransactionsModel
from app.transaction_api.model.account import AccountModel
from app.transaction_api.util.JWTGetters import getCurrentAuthId

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
        currentUserId=getCurrentAuthId()
  
        transactionUserTransfer:list[TransactionsModel]=TransactionsModel.query\
            .join(AccountModel,or_(
                AccountModel.id== TransactionsModel.from_account_id,
                AccountModel.id == TransactionsModel.to_account_id
            ))\
                .filter(AccountModel.user_id ==currentUserId).all()
                
      

        return transactionUserTransfer 
    
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
        except ValueError as E:
            abort(HTTPStatus.NOT_ACCEPTABLE, message={
              "error_text":str(E),
              "available_transaction_type" : ["groceries",
                                              "rent",
                                              "entertainment",
                                              "deposit",
                                              "withdrawal",
                                              "transfer"
                                              ]
          })
      
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
        print(transaction_id)
        return DBS.getDbModal(transaction_id)
    

@blp.route("/transactions/catagories")
class TransactionCategoryViews(MethodView):
    def get(self,transaction_id ):
        """retrieve  a list of transaction catagories"""
        return DBS.getDbModal(transaction_id)
