

from flask_smorest import Blueprint,abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from http import HTTPStatus


from app.transaction_api.service.DbModelService import DbModelService
from app.transaction_api.schemas.account import (
    AccountUpdateSchemas,
    AccountCreateSchemas,
    AccountResponseSchema
    )
from app.transaction_api.model.account import AccountModel


blp= Blueprint("account", __name__,description="""
               account managements 
               """ )

DBS= DbModelService(AccountModel)

@blp.route("/account")
class AccountView(MethodView):
    
    @blp.response(HTTPStatus.OK, AccountResponseSchema(many=True))
    def get(self):
        """retrieve a list of all accounts belonging to the currently authenticated user"""
        return DBS.getDbModalAll()
    
    @blp.arguments(AccountCreateSchemas)
    @blp.response(HTTPStatus.CREATED, AccountResponseSchema)
    def post(self,item_data):
        """create a new account for hte currently authenticated user"""
        try:
            return DBS.addModel(item_data)
        except Exception as  E:            
            abort(HTTPStatus.NOT_ACCEPTABLE, message="failed to create account")
    
@blp.route("/account/<string:account_id>")
class AccountViews(MethodView):
    
    
    @blp.response(HTTPStatus.OK, AccountResponseSchema)
    def get(self,account_id):
        """retrieve details of specific accounts by its id, """
        return DBS.getDbModal(account_id)
    
    @blp.arguments(AccountUpdateSchemas)
    @blp.response(HTTPStatus.ACCEPTED, AccountResponseSchema)
    def put(self,item_data,account_id):
        """update details of an existing account"""
        try:
            return DBS.updateDbModel(account_id,item_data)
        except SQLAlchemyError as  E:
            abort(HTTPStatus.NOT_ACCEPTABLE, message="error while update the animal")
