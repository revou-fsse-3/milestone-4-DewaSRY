
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from http import HTTPStatus
from sqlalchemy.exc import SQLAlchemyError
from http import HTTPStatus
from uuid import UUID


from app.transaction_api.service.DbModelService import DbModelService
from app.transaction_api.schemas.user import (
        UserBaseSchema,
        UseResponseSchema
    )
from app.transaction_api.model.user import UserModel





blp = Blueprint("users", __name__, description="""
                user management end point
                """)

DBS= DbModelService(UserModel)

@blp.route("/user")
class UserViews(MethodView):
    @blp.arguments(UserBaseSchema)
    @blp.response(HTTPStatus.CREATED, UseResponseSchema) 
    def post(self,item_data ):
        """create new user"""
        userMode:UserModel= UserBaseSchema().loads(**item_data)
        try:
            return DBS.addModel(userMode)
        except Exception as  E:
            abort(HTTPStatus.NOT_ACCEPTABLE, message="error while create users ")

@blp.route("/user/<string:user_id>")
class UserViews(MethodView): 
    @blp.response(HTTPStatus.Ok, UseResponseSchema) 
    def get(self,user_id ):
        pass
        return DBS.getDbModal(user_id)
    
    @blp.arguments(UserBaseSchema)
    @blp.response(HTTPStatus.ACCEPTED, UseResponseSchema)
    def put(self,item_id,item_data):
        """update the profile information of currently authenticated"""
        try:
            return DBS.updateDbModel(item_id,item_data)
        except SQLAlchemyError as  E:
            abort(HTTPStatus.NOT_ACCEPTABLE, message="error while update the animal")
