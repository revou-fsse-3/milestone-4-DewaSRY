
from flask_smorest import Blueprint
from flask.views import MethodView


blp= Blueprint("transactions", __name__, description="""transaction management """)

@blp.route("/transactions")
class TransactionView(MethodView):
    def get():
        """Retrieve a list of all transaction for the currently authenticated user's account """
        pass
        
    def post():
        """Initiate a new transactions (deposit, withdrawal or transfer )"""


@blp.route("/transactions/<string:transaction_id>")
class TransactionViews(MethodView):
    def get():
        """retrieval details of specific transaction by its ID"""