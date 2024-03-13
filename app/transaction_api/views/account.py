

from flask_smorest import Blueprint
from flask.views import MethodView



blp= Blueprint("account", __name__,description="""account managements """ )


@blp.route("/account")
class AccountView(MethodView):
    def get():
        """retrieve a list of all accounts belonging to the currently authenticated user"""
        pass
    def post():
        """create a new account for hte currently authenticated user"""
        pass
    
@blp.route("/account<string:account_id>")
class AccountViews(MethodView):
    def get():
        """retrieve details of specific accounts by its id, """
        pass
    
    def put():
        """update details of an existing account"""
        pass
