
from flask_smorest import Blueprint, abort
from flask.views import MethodView

from http import HTTPStatus


blp = Blueprint("users", __name__, description="""
                user management end point
                """)


@blp.route("/user")
class UserViews(MethodView): 
    def post():
        """create new user"""
        pass

@blp.route("/user/<string:user_id>")
class UserViews(MethodView): 
    def get():
        """retrieve the profile of the currently authenticated user"""
        pass
    def put():
        """update the profile information of currently authenticated"""
