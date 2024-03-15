
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from http import HTTPStatus
from flask_jwt_extended import jwt_required
from sqlalchemy import or_
from app.transaction_api.service.DbModelService import DbModelService
from app.transaction_api.schemas.transaction import (
        TransactionsResponseSchema,
        TransactionCreateSchemas,
        TransactionPayloadSchemas,
        TransactionCategoryListSchemas
    )

from app.transaction_api.model.transaction import TransactionsModel
from app.transaction_api.model.transaction_categories import TransactionCategoryModel
from app.transaction_api.model.account import AccountModel
from app.transaction_api.util.JWTGetters import getCurrentAuthId
from app.transaction_api.util.db import TRANSACTION_TYPE_LIST
from app.transaction_api.doc.transaction import (
    ERROR_TRANSACTION_LIST,
    ERROR_TRANSACTION_NOT_FOUND,
    ERROR_TRANSACTION_CATEGORY_NOT_FOUND,
    ERROR_CREATE_TRANSACTION)
blp= Blueprint("transactions", __name__, description="""
               transaction management 
               """)
DBS= DbModelService(TransactionsModel)

@blp.route("/transactions")
class TransactionView(MethodView):
    
    @jwt_required()
    @blp.response(HTTPStatus.OK, TransactionsResponseSchema(many=True))
    @blp.alt_response(HTTPStatus.NOT_FOUND,
                      example=ERROR_TRANSACTION_LIST,
                      description="current user have not transaction list" )
    def get(self):
        """Retrieve a list of all transaction for the currently authenticated user's account """
        currentUserId=getCurrentAuthId()
  
        transactionList:list[TransactionsModel]=TransactionsModel.query\
            .join(AccountModel,or_(
                AccountModel.id== TransactionsModel.from_account_id,
                AccountModel.id == TransactionsModel.to_account_id
            ))\
                .filter(AccountModel.user_id ==currentUserId).all()
        if len(transactionList) == 0:
            abort(HTTPStatus.NOT_FOUND, message={
                "error":"current account have no transaction history"
            })
        return transactionList 
    
    @jwt_required()
    @blp.arguments(TransactionPayloadSchemas)
    @blp.response(HTTPStatus.CREATED, TransactionsResponseSchema)
    @blp.alt_response(HTTPStatus.NOT_ACCEPTABLE, 
                      example=ERROR_CREATE_TRANSACTION,
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
              "available_transaction_type" :TRANSACTION_TYPE_LIST
          })
      
        try:
            return DBS.addModel(transactionModel)
        except Exception as  E:
            abort(HTTPStatus.NOT_ACCEPTABLE, message="error while insert the animal")

@blp.route("/transactions/<string:transaction_id>")
class TransactionViews(MethodView):
    @jwt_required()
    @blp.response(HTTPStatus.OK, TransactionsResponseSchema)
    @blp.alt_response(HTTPStatus.NOT_ACCEPTABLE, 
                    example=ERROR_TRANSACTION_NOT_FOUND,
                    description="transaction not found",
                    )
    def get(self,transaction_id ):
        """retrieval details of specific transaction by its ID"""
        try:
            return DBS.getDbModal(transaction_id)
        except Exception as e:
            abort(HTTPStatus.NOT_FOUND ,message="transaction not found")
    

@blp.route("/transactions/catagories")
class TransactionCategoryViews(MethodView):
    @jwt_required()
    @blp.response(HTTPStatus.OK, TransactionCategoryListSchemas(many=True))
    @blp.alt_response(HTTPStatus.NOT_ACCEPTABLE, 
                example=ERROR_TRANSACTION_CATEGORY_NOT_FOUND,
                description="transaction not found",
                )
    @blp.alt_response(HTTPStatus.NOT_FOUND, 
                example=ERROR_TRANSACTION_NOT_FOUND,
                description="user does't have any transaction  records",
                )
    def get(self):
        """retrieve  a list of transaction catagories for budgeting purpose (have budget type)"""
        currentUserId=getCurrentAuthId()
        categoryTransactionList=TransactionCategoryModel.query\
            .join(TransactionsModel, TransactionsModel.type_id== TransactionCategoryModel.id)\
            .join(AccountModel,or_(
                AccountModel.id== TransactionsModel.from_account_id,
                AccountModel.id == TransactionsModel.to_account_id
            ))\
            .filter(AccountModel.user_id ==currentUserId).all()
        if len(categoryTransactionList) == 0:
            abort(HTTPStatus.NOT_FOUND, message="user does't have any transaction  records")
        return categoryTransactionList 
