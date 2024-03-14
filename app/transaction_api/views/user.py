
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
from app.transaction_api.util.JWTGetters import getCurrentAuthId

blp = Blueprint("users", __name__, description="""
                user management end point
                """)

DBS= DbModelService(UserModel)

@blp.route("/user")
class UserViews(MethodView):
    
    @jwt_required()
    @blp.response(HTTPStatus.OK, UseResponseSchema(many=True)) 
    def get(self):
        """retrieve all users """
        id=getCurrentAuthId()
        print(id)
        return DBS.getDbModalAll()
    
    @blp.arguments(UserCreateSchema)
    @blp.response(HTTPStatus.CREATED, UseResponseSchema) 
    def post(self,item_data):
        """create new user"""
        try:
            return DBS.addModel(item_data)
        except Exception as  E:
            abort(HTTPStatus.NOT_ACCEPTABLE, message="error while create users ")

@blp.route("/user/<string:user_id>")
class UserViews(MethodView): 
    
    @jwt_required()
    @blp.response(HTTPStatus.OK, UseResponseSchema) 
    def get(self,user_id ):
        """retrieve the profile of the currently authenticated user"""
        return DBS.getDbModal(user_id)
    
    @jwt_required()
    @blp.arguments(UserPayloadSchema)
    @blp.response(HTTPStatus.ACCEPTED, UseResponseSchema)
    def put(self,item_data,user_id):
        """update the profile information of currently authenticated"""
        try:
            return DBS.updateDbModel(user_id,item_data)
        except SQLAlchemyError as  E:
            abort(HTTPStatus.NOT_ACCEPTABLE, message="error while update the animal")



@blp.route("/login")
class UserLogin(MethodView):
    
    @blp.arguments(LoginSchemas)
    def post(self, user_data):
        """user login to get the access token, access token will valid for 7 days"""
        user:UserModel = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id,fresh=True, expires_delta=timedelta(days=7) )
            return {"access_token": access_token, }

        abort(401, message="Invalid credentials.")
