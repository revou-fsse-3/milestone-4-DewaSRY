
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from http import HTTPStatus
from sqlalchemy.exc import SQLAlchemyError
from http import HTTPStatus


from app.transaction_api.service.DbModelService import DbModelService
from app.transaction_api.schemas.user import (
        UserBaseSchema,
        UseResponseSchema,
        UserUpdateSchema
    )
from app.transaction_api.model.user import UserModel





blp = Blueprint("users", __name__, description="""
                user management end point
                """)

DBS= DbModelService(UserModel)

@blp.route("/user")
class UserViews(MethodView):
    @blp.response(HTTPStatus.OK, UseResponseSchema(many=True)) 
    def get(self):
        return DBS.getDbModalAll()
    
    @blp.arguments(UserBaseSchema)
    @blp.response(HTTPStatus.CREATED, UseResponseSchema) 
    def post(self,item_data):
        """create new user"""
        try:
            return DBS.addModel(item_data)
        except Exception as  E:
            abort(HTTPStatus.NOT_ACCEPTABLE, message="error while create users ")

@blp.route("/user/<string:user_id>")
class UserViews(MethodView): 
    @blp.response(HTTPStatus.OK, UseResponseSchema) 
    def get(self,user_id ):
        """retrieve the profile of the currently authenticated user"""
        return DBS.getDbModal(user_id)
    
    @blp.arguments(UserUpdateSchema)
    @blp.response(HTTPStatus.ACCEPTED, UseResponseSchema)
    def put(self,item_data,user_id):
        """update the profile information of currently authenticated"""
        print(item_data)
        print(user_id)
        try:
            return DBS.updateDbModel(user_id,item_data)
        except SQLAlchemyError as  E:
            abort(HTTPStatus.NOT_ACCEPTABLE, message="error while update the animal")
