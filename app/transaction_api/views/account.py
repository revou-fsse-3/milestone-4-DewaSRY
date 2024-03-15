

from flask_smorest import Blueprint,abort
from flask import jsonify
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from http import HTTPStatus
from flask_jwt_extended import jwt_required


from app.transaction_api.service.DbModelService import DbModelService
from app.transaction_api.schemas.account import (
    AccountBaseSchemas,
    AccountCreateSchemas,
    AccountResponseSchema,
    AccountPayloadSchemas
    )
from app.transaction_api.model.account import AccountModel
from app.transaction_api.model.account_type import AcountTypeModel
from app.transaction_api.util.JWTGetters import getCurrentAuthId
from app.transaction_api.util.db import ACCOUNT_TYPE_LIST,TRANSACTION_TYPE_LIST

blp= Blueprint("account", __name__,description="""
               account managements 
               """ )

DBS= DbModelService(AccountModel)

@blp.route("/account")
class AccountView(MethodView):
    
    @jwt_required()
    @blp.response(HTTPStatus.OK, AccountResponseSchema(many=True))
    @blp.alt_response(status_code= HTTPStatus.NOT_FOUND, description="user does't have any account")
    @blp.alt_response(status_code= HTTPStatus.INTERNAL_SERVER_ERROR, description="server error while query user account ")
    def get(self):
        """retrieve a list of all accounts belonging to the currently authenticated user"""
        authId= getCurrentAuthId()
        allAcount:list[AccountModel]=AccountModel.query.filter(AccountModel.user_id == authId).all()
        try:
            allAcount:list[AccountModel]=AccountModel.query.filter(AccountModel.user_id == authId).all()
        except Exception as e:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="failed to query all acount belonging the user")
        if len(allAcount) ==0:
            abort(HTTPStatus.NOT_FOUND, message="user does't have any account")
        
        return allAcount
            
    
    @jwt_required()
    @blp.arguments(AccountBaseSchemas)
    @blp.response(HTTPStatus.CREATED, AccountResponseSchema)
    @blp.alt_response(status_code= HTTPStatus.INTERNAL_SERVER_ERROR, description="server error while create account or inserting account to data base")
    @blp.alt_response(status_code= HTTPStatus.NOT_ACCEPTABLE, description="""
                      there is some issue while create account model, there is might be some error while looking for match account type
                      """)
    def post(self,user_data):
        """create a new account for hte currently authenticated user"""
        schemasCreate= AccountCreateSchemas()
        authId= getCurrentAuthId()
        accountModel:AccountModel
        try:
          accountModel:AccountModel= schemasCreate.load({
              "user_id":authId,
              **user_data
          })
        except ValueError as E:
          abort(HTTPStatus.NOT_ACCEPTABLE, message={
              "error_text":str(E),
              "available_acount_type" : ACCOUNT_TYPE_LIST
          })
        try:
            return DBS.addModel(accountModel)
        except Exception as  E:            
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="failed to insert account account")
    
@blp.route("/account/<string:account_id>")
class AccountViews(MethodView):
    
    @jwt_required()
    @blp.response(HTTPStatus.OK, AccountResponseSchema)
    def get(self,account_id):
        """retrieve details of specific accounts by its id, """
        return DBS.getDbModal(account_id)
    
    @jwt_required()
    @blp.arguments(AccountBaseSchemas)
    @blp.response(HTTPStatus.ACCEPTED, AccountResponseSchema)
    def put(self,item_data,account_id):
        """update details of an existing account"""
        try:
            return DBS.updateDbModel(account_id,item_data)
        except Exception as  E:
            abort(HTTPStatus.NOT_ACCEPTABLE, message={
              "error_text":str(E),
              "available_acount_type" : ["checking","saving" ]
          })
    @jwt_required()
    def delete(self,account_id):
        "delete account "
        DBS.deleteDbModal(account_id)
        return {"message": "account deleted."},HTTPStatus.OK