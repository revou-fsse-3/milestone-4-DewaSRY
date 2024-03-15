
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from http import HTTPStatus
from sqlalchemy.exc import SQLAlchemyError
from http import HTTPStatus
from passlib.hash import pbkdf2_sha256
from datetime import timedelta
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
)

from app.transaction_api.service.DbModelService import DbModelService
from app.transaction_api.schemas.user import (
        UserCreateSchema,
        UseResponseSchema,
        UserPayloadSchema,
        LoginSchemas
    )
from app.transaction_api.model.user import UserModel
from app.transaction_api.doc.user import ERROR_DUPLICATE_USER,ERROR_USER_NOT_FOUND,ERROR_INVALID_CREDENTIAL
blp = Blueprint("users", __name__, description="""
                user management end point
                """)

DBS= DbModelService(UserModel)

@blp.route("/user")
class UserViews(MethodView):

    @blp.arguments(UserCreateSchema)
    @blp.response(HTTPStatus.CREATED, UseResponseSchema) 
    @blp.alt_response(HTTPStatus.CONFLICT,
                      example=ERROR_DUPLICATE_USER,
                      description="duplicate username")
    def post(self,item_data):
        """create new user"""
        try:
            return DBS.addModel(item_data)
        except Exception as  E:
            abort(HTTPStatus.CONFLICT, message="error while create: duplicate user name")

@blp.route("/user/<string:user_id>")
class UserViews(MethodView): 
    
    @jwt_required()
    @blp.response(HTTPStatus.OK, UseResponseSchema) 
    @blp.alt_response(HTTPStatus.CONFLICT,
                      example=ERROR_USER_NOT_FOUND,
                      description="user not found")
    def get(self,user_id ):
        """retrieve the profile of the currently authenticated user"""
        try:
            return DBS.getDbModal(user_id)
        except Exception as E:
            abort(HTTPStatus.NOT_FOUND, message="user not found")
            
    
    @jwt_required()
    @blp.arguments(UserPayloadSchema)
    @blp.response(HTTPStatus.ACCEPTED, UseResponseSchema)
    @blp.alt_response(HTTPStatus.CONFLICT,
                      description="error while update the animal")
    def put(self,item_data,user_id):
        """update the profile information of currently authenticated"""
        try:
            return DBS.updateDbModel(user_id,item_data)
        except SQLAlchemyError as  E:
            abort(HTTPStatus.CONFLICT, message="error while update the animal")

@blp.route("/login")
class UserLogin(MethodView):
    
    @blp.arguments(LoginSchemas)
    @blp.alt_response(HTTPStatus.UNAUTHORIZED,
                    example=ERROR_INVALID_CREDENTIAL,
                    description="user not found")
    def post(self, user_data):
        """user login to get the access token, access token will valid for 7 days"""
        user:UserModel = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id,fresh=True, expires_delta=timedelta(days=7) )
            return {"access_token": access_token, }

        abort(HTTPStatus.UNAUTHORIZED, message="Invalid credentials")
