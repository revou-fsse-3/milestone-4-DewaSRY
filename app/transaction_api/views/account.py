

from flask_smorest import Blueprint,abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from http import HTTPStatus


from app.transaction_api.service.DbModelService import DbModelService
from app.transaction_api.schemas.account import (
    AccountBaseSchemas,
    AccountResponseSchema,
    AccountUpdateSchemas
    )
from app.transaction_api.model.account import AccountModel


blp= Blueprint("account", __name__,description="""account managements """ )

DBS= DbModelService(AccountModel)

@blp.route("/account")
class AccountView(MethodView):
    @blp.response(HTTPStatus.OK, AccountResponseSchema)
    def get(self):
        """retrieve a list of all accounts belonging to the currently authenticated user"""
        return DBS.getDbModalAll()
    
    @blp.arguments(AccountBaseSchemas)
    @blp.response(HTTPStatus.CREATED, AccountResponseSchema)
    def post(self,item_data):
        """create a new account for hte currently authenticated user"""
        user:AccountModel= AccountBaseSchemas().loads(**item_data)
        try:
            return DBS.addModel(user)
        except Exception as  E:
            abort(HTTPStatus.NOT_ACCEPTABLE, message="error while insert the animal")
    
@blp.route("/account<string:account_id>")
class AccountViews(MethodView):
    
    @blp.response(HTTPStatus.OK, AccountResponseSchema)
    def get(self,item_id):
        """retrieve details of specific accounts by its id, """
        return DBS.getDbModal(item_id)
    
    @blp.arguments(AccountUpdateSchemas)
    @blp.response(HTTPStatus.ACCEPTED, AccountResponseSchema)
    def put(self,item_data,item_id):
        """update details of an existing account"""
        try:
            return DBS.updateDbModel(item_id,item_data)
        except SQLAlchemyError as  E:
            abort(HTTPStatus.NOT_ACCEPTABLE, message="error while update the animal")
