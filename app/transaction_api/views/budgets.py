



from flask_smorest import Blueprint, abort
from flask.views import MethodView
from http import HTTPStatus
from flask_jwt_extended import jwt_required

from app.transaction_api.service.DbModelService import DbModelService
from app.transaction_api.schemas.budgets import (
        BudgetBaseSchemas,
        BudgetCreateSchemas,
        BudgetResponseSchemas
    )

from app.transaction_api.model.budgets import BudgetsModel
from app.transaction_api.model.account import AccountModel
from app.transaction_api.util.JWTGetters import getCurrentAuthId

blp= Blueprint("budgets", __name__, description="""
               budgets management 
               """)
DBS= DbModelService(BudgetsModel)


@blp.route("/budgets")
class BudgetsViews(MethodView):
    @jwt_required()
    @blp.arguments(BudgetBaseSchemas)
    @blp.response(HTTPStatus.CREATED,BudgetResponseSchemas)
    def post(self, budget_data):
        "Create a new budgets for specific category"
        createSchemas=BudgetCreateSchemas()
        currentId=getCurrentAuthId()
        budgetModel= createSchemas.load({
            **budget_data,
            'user_id':currentId
        })
        return DBS.addModel(budgetModel)
    
    @jwt_required()
    @blp.response(HTTPStatus.OK,BudgetResponseSchemas(many=True))
    def get(self):
        "Retrieve all budgets crete by the user"
        currentId=getCurrentAuthId()
        budgetList= BudgetsModel.query.filter(BudgetsModel.user_id== currentId).all()
        if len(budgetList) == 0:
            abort(HTTPStatus.CONFLICT ,message="current user does't have any budget" )
        return budgetList
               

@blp.route("/budgets/<string:budgets_id>")
class BudgetViews(MethodView):
    @jwt_required()
    @blp.arguments(BudgetBaseSchemas)
    @blp.response(HTTPStatus.CREATED,BudgetResponseSchemas)
    def put(self, budget_data,budgets_id):
        "update an existing budgets"
        try: 
            return DBS.updateDbModel(budgets_id, budget_data)
        except Exception :
            abort(HTTPStatus.CONFLICT,message="failed while updating budget" )